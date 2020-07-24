import copy
import datetime

start_position = {
  'WP8': {'name': 'WP8', 'color': 'white', 'location': '01', 'pic':'WP.png', 'notMoved': True},
  'WP7': {'name': 'WP7', 'color': 'white', 'location': '11', 'pic':'WP.png', 'notMoved': True},
  'WP6': {'name': 'WP6', 'color': 'white', 'location': '21', 'pic':'WP.png', 'notMoved': True},
  'WP5': {'name': 'WP5', 'color': 'white', 'location': '31', 'pic':'WP.png', 'notMoved': True},
  'WP4': {'name': 'WP4', 'color': 'white', 'location': '41', 'pic':'WP.png', 'notMoved': True},
  'WP3': {'name': 'WP3', 'color': 'white', 'location': '51', 'pic':'WP.png', 'notMoved': True},
  'WP2': {'name': 'WP2', 'color': 'white', 'location': '61', 'pic':'WP.png', 'notMoved': True},
  'WP1': {'name': 'WP1', 'color': 'white', 'location': '71', 'pic':'WP.png','notMoved': True},
  'BP8': {'name': 'BP8', 'color': 'black', 'location': '06', 'pic':'BP.png', 'notMoved': True},
  'BP1': {'name': 'BP1', 'color': 'black', 'location': '16', 'pic':'BP.png', 'notMoved': 'true'},
  'BP2': {'name': 'BP2', 'color': 'black', 'location': '26', 'pic':'BP.png', 'notMoved': True},
  'BP3': {'name': 'BP3', 'color': 'black', 'location': '36', 'pic':'BP.png', 'notMoved': True},
  'BP4': {'name': 'BP4', 'color': 'black', 'location': '46', 'pic':'BP.png', 'notMoved': True},
  'BP5': {'name': 'BP5', 'color': 'black', 'location': '56', 'pic':'BP.png', 'notMoved': True},
  'BP6': {'name': 'BP6', 'color': 'black', 'location': '66', 'pic':'BP.png', 'notMoved': True},
  'BP7': {'name': 'BP7', 'color': 'black', 'location': '76', 'pic':'BP.png', 'notMoved': True},
  'WR1': {'name': 'WR1', 'color': 'white', 'location': '00', 'pic':'WR.png', 'notMoved': True},
  'WR2': {'name': 'WR2', 'color': 'white', 'location': '70', 'pic':'WR.png', 'notMoved': True},
  'BR1': {'name': 'BR1', 'color': 'black', 'location': '07', 'pic':'BR.png', 'notMoved': True},
  'BR2': {'name': 'BR2', 'color': 'black', 'location': '77', 'pic':'BR.png', 'notMoved': True},
  'WB1': {'name': 'WB1', 'color': 'white', 'location': '10', 'pic':'WB.png', 'notMoved': True},
  'WB2': {'name': 'WB2', 'color': 'white', 'location': '60', 'pic':'WB.png', 'notMoved': True},
  'BB1': {'name': 'BB1', 'color': 'black', 'location': '17', 'pic':'BB.png', 'notMoved': True},
  'BB2': {'name': 'BB2', 'color': 'black', 'location': '67', 'pic':'BB.png', 'notMoved': True},
  'WKN1': {'name': 'WKN1', 'color': 'white', 'location': '20', 'pic':'WK.png', 'notMoved': True},
  'WKN2': {'name': 'WKN2', 'color': 'white', 'location': '50', 'pic':'WK.png', 'notMoved': True},
  'BKN1': {'name': 'BKN1', 'color': 'black', 'location': '27', 'pic':'BK.png', 'notMoved': True},
  'BKN2': {'name': 'BKN2', 'color': 'black', 'location': '57', 'pic':'BK.png', 'notMoved': True},
  'WQ': {'name': 'WQ', 'color': 'white', 'location': '30', 'pic':'WQ.png', 'notMoved': True},
  'BQ': {'name': 'BQ', 'color': 'black', 'location': '37', 'pic':'BQ.png', 'notMoved': True},
  'BKing': {'name': 'BKing', 'color': 'black', 'location': '47', 'pic':'BKing.png', 'notMoved': True, 'check': False},
  'WKing': {'name': 'WKing', 'color': 'white', 'location': '40', 'pic':'WKing.png', 'notMoved': True, 'check': False}
}

def sanity(x, y):
  if x<8 and x>=0 and y<8 and y>=0:
    return  str(x) + str(y)

def ocupied(position, loc):
  for key in position:
    if position[key]['location'] == loc:
      return position[key]['name'][0]
  if loc:
    return False
  return 'Not'


def check_king(position):
  white_state = position['WKing']['location']
  black_state = position['BKing']['location']
  for key in position:
    if position[key]['name'][0] == 'W' and black_state in position[key]['location']:
      position['BKing']['check'] == True
  for key in position:
    if position[key]['name'][0] == 'B' and black_state in position[key]['location']:
      position['WKing']['check'] == True
  return position

def save_king(position, key, move):
  position2 = copy.deepcopy(position)
  position2[key]['moves'].append(move)
  testdict = calculate(position2, 'W')
  if not testdict['WKing']['check']:
    position[key]['moves'].append(move)
  return position

def straight_move_test(position, key, x, y, enemy):
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y)):
      position[key]['moves'].append(sanity(x+i, y))
    else:
      if ocupied(position, sanity(x+i, y)) == enemy:
        position[key]['moves'].append(sanity(x+i, y))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y)):
      position[key]['moves'].append(sanity(x-i, y))
    else:
      if ocupied(position, sanity(x-i, y)) == enemy:
        position[key]['moves'].append(sanity(x-i, y))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x, y+i)):
      position[key]['moves'].append(sanity(x, y+i))
    else:
      if ocupied(position, sanity(x, y+i)) == enemy:
        position[key]['moves'].append(sanity(x, y+i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x, y-i)):
      position[key]['moves'].append(sanity(x, y-i))
    else:
      if ocupied(position, sanity(x, y-i)) == enemy:
        position[key]['moves'].append(sanity(x, y-i))
      break
  return position

def straight_move(position, key, x, y, enemy):
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y)):
      position = save_king(position, key, sanity(x+i, y))
    else:
      if ocupied(position, sanity(x+i, y)) == enemy:
        position = save_king(position, key, sanity(x+i, y))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y)):
      position = save_king(position, key, sanity(x-i, y))
    else:
      if ocupied(position, sanity(x-i, y)) == enemy:
        position = save_king(position, key, sanity(x-i, y))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x, y+i)):
      position = save_king(position, key, sanity(x, y+i))
    else:
      if ocupied(position, sanity(x, y+i)) == enemy:
        position = save_king(position, key, sanity(x, y+i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x, y-i)):
      position = save_king(position, key, sanity(x, y-i))
    else:
      if ocupied(position, sanity(x, y-i)) == enemy:
        position = save_king(position, key, sanity(x, y-i)) 
      break
  return position

def calculate(position, color):
  for key in position:
    if position[key]['location'] == 'whiteHolder' or  position[key]['location'] == 'blackHolder':
      continue
    position[key]['moves'] = []
    x = int(position[key]['location'][0])
    y = int(position[key]['location'][1])
    # WHITE POWN
    if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'W' and position[key]['name'][0] != color:
      if not ocupied(position, sanity(x, y+1)):
        position[key]['moves'].append(sanity(x, y+1))
      if position[key]['notMoved'] and not ocupied(sanity(x, y+2)):
        position[key]['moves'].append(sanity(x, y+2))
      if ocupied(position, sanity(x+1, y+1)) == 'B':
        position[key]['moves'].append(sanity(x+1, y+1))
      if ocupied(position, sanity(x-1, y+1)) == 'B':
        position[key]['moves'].append(sanity(x-1, y+1))
    # BLACK POWN
    if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'B' and position[key]['name'][0] != color:
      if not ocupied(position, sanity(x, y-1)):
        position[key]['moves'].append(sanity(x, y-1))
      if position[key]['notMoved'] and not ocupied(position, sanity(x, y-2)):
        position[key]['moves'].append(sanity(x, y-2))
      if ocupied(position, sanity(x+1, y-1)) == 'W':
        position[key]['moves'].append(sanity(x+1, y-1))
      if ocupied(position, sanity(x-1, y-1)) == 'W':
        position[key]['moves'].append(sanity(x-1, y-1))
    # WHITE ROOK
    if position[key]['name'][1] == 'R' and position[key]['name'][0] == 'W':
      position = straight_move_test(position, key, x, y, 'B') 
    # BLACK ROOK
    if position[key]['name'][1] == 'R' and position[key]['name'][0] == 'B':
      position = straight_move_test(position, key, x, y, 'W')

  position = check_king(position)
  return position

def calculate_moves(position=start_position):
  for key in position:
    if position[key]['location'] == 'whiteHolder' or  position[key]['location'] == 'blackHolder':
      continue
    position[key]['moves'] = []
    x = int(position[key]['location'][0])
    y = int(position[key]['location'][1])
    # WHITE POWN
    if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'W':

      if not ocupied(position, sanity(x, y+1)):
        position = save_king(position, key, sanity(x, y+1))
      if position[key]['notMoved'] and not ocupied(position, sanity(x, y+2)):
        position = save_king(position, key, sanity(x, y+2))
      if ocupied(position, sanity(x+1, y+1)) == 'B':
        position = save_king(position, key, sanity(x+1, y+1))
      if ocupied(position, sanity(x-1, y+1)) == 'B':
        position = save_king(position, key, sanity(x-1, y+1))
    # BLACK POWN
    if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'B':
      if not ocupied(position, sanity(x, y-1)):
        position = save_king(position, key, sanity(x, y-1))
      if position[key]['notMoved'] and not ocupied(position, sanity(x, y-2)):
        position = save_king(position, key, sanity(x, y-2))
      if ocupied(position, sanity(x+1, y-1)) == 'W':
        position = save_king(position, key, sanity(x+1, y-1))
      if ocupied(position, sanity(x-1, y-1)) == 'W':
        position = save_king(position, key, sanity(x-1, y-1))
    # WHITE ROOK
    if position[key]['name'][1] == 'R' and position[key]['name'][0] == 'W':
      position = straight_move(position, key, x, y, 'B') 
    # BLACK ROOK
    if position[key]['name'][1] == 'R' and position[key]['name'][0] == 'B':
      position = straight_move(position, key, x, y, 'W')

  position = check_king(position)
  return position


def attac(move, position):
  for key in position:
    if position[key]['location'] == move:
      if position[key]['color'] == 'white':
        return {'figure': position[key]['name'], 'holder':'whiteHolder'}
      else:
        return {'figure': position[key]['name'], 'holder':'blackHolder'}

def time_master(time, white, black, move):
  now = datetime.datetime.utcnow()
  diff = now - time
  if move == 'white':
    white = diff.total_seconds() - black
  else:
    black = diff.total_seconds() - white
  return {'white': white, 'black': black}