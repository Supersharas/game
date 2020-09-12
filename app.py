from flask import Flask, url_for, jsonify, request, session, redirect
from flask import render_template
from sqlalchemy import or_
import sys
import json
import hashlib
from markupsafe import escape

from chessEngine import reffery, calculate_moves

from models import setup_db, Game, Player, State, Offer, db

app = Flask(__name__,
static_folder='static' )
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
salt = b'\xb1\xc6\xd4\xe8[\xae\xdc\xb7\xb6\xb9h\x90\xda3J$`8\x04\x1e'
app.debug = True

setup_db(app)

# CASH ONLY FOR DEVELOPMENT
returned = []
games = {}

def cash_get(game, move_n):
  for key in games:
    if key == game:
      if games[key] == move_n:
        returned.append('yes')
        return True
  games[game] = move_n
  return False

def cash_put(user, move_n):
  games[user] = move_n

@app.route('/cash')
def check_cash():
  return render_template('cash.html',ret=returned, games=games)

@app.route('/')
def hello_world():
    return render_template('testStartPage.html')

@app.route('/jsdemo')
def jsdemo():
  return render_template('demo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = False
  wrong_user = False
  wrong_password = False
  please_enter = False
  if request.method == 'POST':
    content = request.form
    username = request.form.get('userName')
    password = request.form.get('password')
    pa = password.encode()
    h = hashlib.sha256(pa + salt).hexdigest()
    if username and password:
      try:
        player = Player.query.filter_by(name=username).first()
        if player:
          if player.password != h:
            wrong_password = 'Wrong password'
        else:
          wrong_user = "Username does not exists on our records"
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()
    else:
      please_enter = 'Please prowide user name and password!'
    if error:
      return render_template('login.html')
    else:
      return redirect(url_for('chess'))

  return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
  error = False
  username = request.form.get('userName')
  password2 = request.form.get('repeatPassword')
  password = request.form.get('password')
  if username and password and password2:
    if password == password2:
      try:
        pa = password.encode()
        h = hashlib.sha256(pa + salt).hexdigest()
        player = Player(name=username, password=h) 
        Player.insert(player)
        answer = player.format()
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()

  return answer


@app.route('/startGame/<int:offer>')
def start_game(offer):
  error = False
  try:
    if 'userId' in session:
      player_id = session['userId']
    else:
      player = Player()
      Player.insert(player)
      player_id = player.id
      session['userId'] = player.id
    offer = Offer.query.filter_by(id=offer).first()
    new_game = Game(player_one=offer.player_one, player_two = player_id)
    Game.insert(new_game)
    game = new_game.id
    offer.delete()
    current_state = State(game_id=new_game.id, move_number=1,move='white',position=calculate_moves())
    State.insert(current_state)
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    return 'start game error'
  else:
    return redirect(url_for('white', game = game))

@app.route('/chess/move', methods=['GET', 'POST'])
def move():
  error = False
  if request.method == 'POST':
    content = json.loads(request.data)
    figure = content.get('figure', None)
    move_number = content.get('moveNumber', None)
    gameId = content.get('gameId', None)
    if figure:
      if session['userId']:
        state = State.query.join(Game).filter(or_(Game.player_one==session['userId'], Game.player_two==session['userId'])).order_by(State.move_number.desc()).first()
        legal_move = reffery(state, figure, content['move'])
        if legal_move:
          try:
            next_state = State(game_id=state.game_id, move_number=state.move_number+1, move=legal_move['next_move'], position=legal_move['new_position'], 
            white_timer=legal_move['time']['white'], black_timer=legal_move['time']['black'])
            State.insert(next_state)
            data = next_state.format()
            cash_put(state.game_id, state.move_number+1)
          except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
          finally:
            db.session.close()
          if error:
            return json.dumps({'error': True})
          return json.dumps(data)
        else:
          return json.dumps({'not': 'your move'})
    if move_number:
      if session['userId']:
        cashed = cash_get(gameId, move_number)
        if cashed:
          return json.dumps(None)
        state = State.query.join(Game).filter(or_(Game.player_one==session['userId'], Game.player_two==session['userId'])).order_by(State.move_number.desc()).first()
        new_state = state.format()
        db.session.close()
        if move_number < new_state['move_number']:
          return json.dumps(new_state)
        else:
          return json.dumps(None)
  else:
    return json.dumps({'kas': 'per huiniene'})

@app.route('/test')
def test():
  player = Player()
  Player.insert(player)
  session['userId'] = player.id
  oponent = Player()
  Player.insert(oponent)
  new_game = Game(player_one=player.id, player_two = oponent.id)
  Game.insert(new_game)
  game = new_game.id
  current_state = State(game_id=new_game.id, move_number=1,move='white',position=calculate_moves())
  State.insert(current_state)
  player1 = current_state.games.player
  oponent1 = current_state.games.oponent
  data = current_state.format()
  db.session.close()
  return render_template('white.html', data=json.dumps(data), player=player1, oponent=oponent1, game=game)
  
@app.route('/chess/black/<int:game>')
def black(game):
  state = State.query.filter_by(game_id=game).order_by(State.move_number.desc()).first()
  data = state.format()
  player = state.games.player
  oponent = state.games.oponent
  # ONLY FOR TESTING
  session['userId'] = oponent.id
  db.session.close()
  return render_template('black.html', data=json.dumps(data), player=oponent, oponent=player,)

@app.route('/chess/white/<int:game>')
def white(game):
  state = State.query.filter_by(game_id=game).order_by(State.move_number.desc()).first()
  data = state.format()
  player = state.games.player
  # ONLY FOR TESTING
  session['userId'] = player.id
  oponent = state.games.oponent
  #time_test = time_master(state.date, state.white_timer, state.black_timer, move)
  db.session.close()
  return render_template('white.html', data=json.dumps(data), player=player, oponent=oponent,)#, time=time_test)

@app.route('/chess')
def chess():
  my_game = ''
  if 'userId' in session:
    games = Offer.query.filter(Offer.player_one!=session['userId']).all()
    my_game = Offer.query.filter_by(player_one=session['userId']).first()
  else:
    games = Offer.query.all()
  test = False
  if 'userId' in session:
    test = True
  db.session.close()
  return render_template('startGame.html', offers=games, test=test, my_game=my_game)

@app.route('/offer')
def offer():
  error = False
  try:
    player = Player()
    Player.insert(player)
    offer = Offer(player_one = player.id)
    Offer.insert(offer)
    session['userId'] = player.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    return 'offer error'
  else:
    return redirect(url_for('chess'))
  
  #return jsonify(offer.format())

@app.route('/chess/lobby')
def lobby():
  nice_game = 'none'
  nice_offers = []
  offers = Offer.query.all()
  if 'userId' in session:
    my_game = Game.query.filter_by(player_one=session['userId']).first()
    if my_game:
      nice_game = my_game.format()
  for offer in offers:
    nice_offers.append(offer.format())
  db.session.close()
  return jsonify({'offers': nice_offers, 'game' : nice_game})

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('userId', None)
    return redirect(url_for('chess'))
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
  #socketio.run(app, host='0.0.0.0', port=8080)