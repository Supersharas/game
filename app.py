from flask import Flask, url_for, jsonify, request, session, redirect
from flask import render_template
from sqlalchemy import or_
import sys
import json
from markupsafe import escape

from chessEngine import calculate_moves, attac, time_master

from models import setup_db, Game, Player, State, Offer, db

app = Flask(__name__,
static_folder='static' )
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.debug = True

setup_db(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


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
  if request.method == 'POST':
    content = json.loads(request.data)
    figure = content.get('figure', None)
    move_number = content.get('moveNumber', None)
    if figure:
      if session['userId']:
        state = State.query.join(Game).filter(or_(Game.player_one==session['userId'], Game.player_two==session['userId'])).order_by(State.move_number.desc()).first()
        if state.move == state.position[figure]['color']:
          if state.move == 'white':
            next_move = 'black'
          else:
            next_move = 'white'
          if content['move'] in state.position[figure]['moves']:
            temp = state.position
            holder =  attac(content['move'], state.position)
            if holder:
              temp[holder['figure']]['location'] = holder['holder']
            temp[content['figure']]['location'] = content['move']
            temp[content['figure']]['notMoved'] = False
            new_position = calculate_moves(temp)
            time = time_master(state.date, state.white_timer, state.black_timer, state.move)
          next_state = State(game_id=state.game_id, move_number=state.move_number+1, move=next_move, position=new_position, 
            white_timer=time['white'], black_timer=time['black'])
          State.insert(next_state)
          data = next_state.format()
          db.session.close()
          return json.dumps(data)
        else:
          return json.dumps({'not': 'your move'})
    if move_number:
      if session['userId']:
        state = State.query.join(Game).filter(or_(Game.player_one==session['userId'], Game.player_two==session['userId'])).order_by(State.move_number.desc()).first()
        new_state = state.format()
        db.session.close()
        if move_number < new_state['move_number']:
          return json.dumps(new_state)
        else:
        #return json.dumps({'kas': 'per huiniene'})
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
  position = current_state.position
  move = current_state.move
  player1 = current_state.games.player
  oponent1 = current_state.games.oponent
  whiteTimer = current_state.white_timer
  blackTimer = current_state.black_timer
  db.session.close()
  return render_template('white.html', data=json.dumps(position), player=player1, oponent=oponent1, move = json.dumps(move), 
    game=game, move_number = json.dumps(1))
  
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