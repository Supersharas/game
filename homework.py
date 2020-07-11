from flask import Flask, url_for, jsonify, request, session, redirect
from flask import render_template
import sys
import json
from markupsafe import escape

from chessEngine import start_position

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
    current_state = State(game_id=new_game.id, move_number=1,move='white',position=start_position)
    State.insert(current_state)
    data = current_state.position
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    return 'error'
  else:
    return redirect(url_for('black', game = game))

@app.route('/chess/black/<int:game>')
def black(game):
  state = State.query.filter_by(game_id=game).first()
  data = state.position
  player_id = session['userId']
  return render_template('black.html',data=json.dumps(data),user=player_id)

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
    return 'error'
  else:
    return redirect(url_for('chess'))
  
  #return jsonify(offer.format())

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('userId', None)
    return redirect(url_for('chess'))
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)