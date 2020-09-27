
import copy
import datetime

from flask import current_app as app

occupied_old = []
start_position = {
  'WP8': {'enPassant': False, 'name': 'WP8', 'color': 'white', 'location': '01', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP7': {'enPassant': False, 'name': 'WP7', 'color': 'white', 'location': '11', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP6': {'enPassant': False, 'name': 'WP6', 'color': 'white', 'location': '21', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP5': {'enPassant': False, 'name': 'WP5', 'color': 'white', 'location': '31', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP4': {'enPassant': False, 'name': 'WP4', 'color': 'white', 'location': '41', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP3': {'enPassant': False, 'name': 'WP3', 'color': 'white', 'location': '51', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP2': {'enPassant': False, 'name': 'WP2', 'color': 'white', 'location': '61', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP1': {'enPassant': False, 'name': 'WP1', 'color': 'white', 'location': '71', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'BP8': {'enPassant': False, 'name': 'BP8', 'color': 'black', 'location': '06', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP1': {'enPassant': False, 'name': 'BP1', 'color': 'black', 'location': '16', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP2': {'enPassant': False, 'name': 'BP2', 'color': 'black', 'location': '26', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP3': {'enPassant': False, 'name': 'BP3', 'color': 'black', 'location': '36', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP4': {'enPassant': False, 'name': 'BP4', 'color': 'black', 'location': '46', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP5': {'enPassant': False, 'name': 'BP5', 'color': 'black', 'location': '56', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP6': {'enPassant': False, 'name': 'BP6', 'color': 'black', 'location': '66', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP7': {'enPassant': False, 'name': 'BP7', 'color': 'black', 'location': '76', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'WR1': {'name': 'WR1', 'color': 'white', 'location': '00', 'pic':'WR.png', 'notMoved': True, 'moves': []},
  'WR2': {'name': 'WR2', 'color': 'white', 'location': '70', 'pic':'WR.png', 'notMoved': True, 'moves': []},
  'BR1': {'name': 'BR1', 'color': 'black', 'location': '07', 'pic':'BR.png', 'notMoved': True, 'moves': []},
  'BR2': {'name': 'BR2', 'color': 'black', 'location': '77', 'pic':'BR.png', 'notMoved': True, 'moves': []},
  'WB1': {'name': 'WB1', 'color': 'white', 'location': '10', 'pic':'WB.png', 'notMoved': True, 'moves': []},
  'WB2': {'name': 'WB2', 'color': 'white', 'location': '60', 'pic':'WB.png', 'notMoved': True, 'moves': []},
  'BB1': {'name': 'BB1', 'color': 'black', 'location': '17', 'pic':'BB.png', 'notMoved': True, 'moves': []},
  'BB2': {'name': 'BB2', 'color': 'black', 'location': '67', 'pic':'BB.png', 'notMoved': True, 'moves': []},
  'WKN1': {'name': 'WKN1', 'color': 'white', 'location': '20', 'pic':'WK.png', 'notMoved': True, 'moves': []},
  'WKN2': {'name': 'WKN2', 'color': 'white', 'location': '50', 'pic':'WK.png', 'notMoved': True, 'moves': []},
  'BKN1': {'name': 'BKN1', 'color': 'black', 'location': '27', 'pic':'BK.png', 'notMoved': True, 'moves': []},
  'BKN2': {'name': 'BKN2', 'color': 'black', 'location': '57', 'pic':'BK.png', 'notMoved': True, 'moves': []},
  'WQ': {'name': 'WQ', 'color': 'white', 'location': '30', 'pic':'WQ.png', 'notMoved': True, 'moves': []},
  'BQ': {'name': 'BQ', 'color': 'black', 'location': '37', 'pic':'BQ.png', 'notMoved': True, 'moves': []},
  'BKing': {'name': 'BKing', 'color': 'black', 'location': '47', 'pic':'BKing.png', 'notMoved': True, 'check': False, 'moves': []},
  'WKing': {'name': 'WKing', 'color': 'white', 'location': '40', 'pic':'WKing.png', 'notMoved': True, 'check': False, 'moves': []}
}

def sanity(x, y):
  if x<8 and x>=0 and y<8 and y>=0:
    return  str(x) + str(y)
  return False

def ocupied(position, loc):
  for key in position:
    if position[key]['location'] == loc:
      return position[key]['name'][0]
  if loc:
    return False
  return 'Not'

def save_castling(position, key, move, key2, move2):
  position2 = copy.deepcopy(position)
  position2[key]['location'] = move
  position2[key2]['location'] = move2
  color = position2[key]['name'][0]
  testdict = calculate(position2, color)
  if color == 'W' and (testdict['WKing']['check'] == False):
    return True
  elif color == 'B' and (testdict['BKing']['check'] == False):
    return True
  return False

def castling(position):
  if not position['WKing']['check']:
    if position['WKing']['notMoved']:
      if position['WR1']['notMoved']:
        long = True
        for key in position:
          if position[key]['location'] == '10' or position[key]['location'] == '20' or position[key]['location']  == '30':
            long = False
            break
        if long and save_castling(position, 'WKing', '20', 'WR1' , '30'):
          position['WKing']['long'] = True
          position['WKing']['moves'].append('20')
      if position['WR2']['notMoved']:
        short = True
        for key in position:
          if position[key]['location'] == '50' or position[key]['location'] == '60':
            short = False
            break
        if short and save_castling(position, 'WKing', '60', 'WR2' , '50'):
          position['WKing']['short'] = True
          position['WKing']['moves'].append('60')
  if not position['BKing']['check']:
    if position['BKing']['notMoved']:
      if position['BR1']['notMoved']:
        long = True
        for key in position:
          if position[key]['location'] == '17' or position[key]['location'] == '27' or position[key]['location']  == '37':
            long = False
            break
        if long and save_castling(position, 'BKing', '27', 'BR1' , '37'):
          position['BKing']['long'] = True
          position['BKing']['moves'].append('27')
      if position['BR2']['notMoved']:
        short = True
        for key in position:
          if position[key]['location'] == '57' or position[key]['location'] == '67':
            short = False
            break
        if short and save_castling(position, 'BKing', '67', 'BR2' , '57'):
          position['BKing']['short'] = True
          position['BKing']['moves'].append('67')
  return position      

def game_over(position):
  black_surrender = True
  white_surrender = True
  for key in position:
    if position[key]['name'][0] == 'W':
      if position[key]['moves'] != []:
        white_surrender = False
    if position[key]['name'][0] == 'B':
      if position[key]['moves'] != []:
        black_surrender = False
  if position['WKing']['check'] and white_surrender:
    position['WKing']['surrender'] = True;
  if position['BKing']['check'] and black_surrender:
    position['BKing']['surrender'] = True;
  return position
    
def check_king(position):
  white_state = position['WKing']['location']
  black_state = position['BKing']['location']
  for key in position:
    if position[key]['name'][0] == 'W' and black_state in position[key]['moves']:
      position['BKing']['check'] = True
    elif position[key]['name'][0] == 'B' and white_state in position[key]['moves']:
      position['WKing']['check'] = True
  return position

def save_king(position, key, move):
  position2 = copy.deepcopy(position)
  holder =  attac(move, position2)
  if holder:
    position2[holder['figure']]['location'] = holder['holder']
    position2[holder['figure']]['moves'] = []
  position2[key]['location'] = move
  color = position2[key]['name'][0]
  testdict = calculate(position2, color)
  if color == 'W' and (testdict['WKing']['check'] == False):
    position[key]['moves'].append(move)
  elif color == 'B' and (testdict['BKing']['check'] == False):
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

def incline_move_test(position, key, x, y, enemy):
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y+i)):
      position[key]['moves'].append(sanity(x+i, y+i))
    else:
      if ocupied(position, sanity(x+i, y+i)) == enemy:
        position[key]['moves'].append(sanity(x+i, y+i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y-i)):
      position[key]['moves'].append(sanity(x+i, y-i))
    else:
      if ocupied(position, sanity(x+i, y-i)) == enemy:
        position[key]['moves'].append(sanity(x+i, y-i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y-i)):
      position[key]['moves'].append(sanity(x-i, y-i))
    else:
      if ocupied(position, sanity(x-i, y-i)) == enemy:
        position[key]['moves'].append(sanity(x-i, y-i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y+i)):
      position[key]['moves'].append(sanity(x-i, y+i))
    else:
      if ocupied(position, sanity(x-i, y+i)) == enemy:
        position[key]['moves'].append(sanity(x-i, y+i))
      break
  return position

def incline_move(position, key, x, y, enemy):
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y+i)):
      position = save_king(position, key, sanity(x+i, y+i))
    else:
      if ocupied(position, sanity(x+i, y+i)) == enemy:
        position = save_king(position, key, sanity(x+i, y+i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x+i, y-i)):
      position = save_king(position, key, sanity(x+i, y-i))
    else:
      if ocupied(position, sanity(x+i, y-i)) == enemy:
        position = save_king(position, key, sanity(x+i, y-i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y-i)):
      position = save_king(position, key, sanity(x-i, y-i))
    else:
      if ocupied(position, sanity(x-i, y-i)) == enemy:
        position = save_king(position, key, sanity(x-i, y-i))
      break
  for i in range(1, 7):
    if not ocupied(position, sanity(x-i, y+i)):
      position = save_king(position, key, sanity(x-i, y+i))
    else:
      if ocupied(position, sanity(x-i, y+i)) == enemy:
        position = save_king(position, key, sanity(x-i, y+i))
      break
  return position

def calculate(position, color):
  position['WKing']['check'] = False
  position['BKing']['check'] = False
  app.logger.info('pposition: %s' % position)
  for key in position:
    if position[key]['name'][0] != color:
      if position[key]['location'] != 'whiteHolder' and  position[key]['location'] != 'blackHolder':
        position[key]['moves'] = []    
        x = int(position[key]['location'][0])
        y = int(position[key]['location'][1])
        # WHITE POWN
        if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'W':
          if ocupied(position, sanity(x+1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x+1, y+1))
          if ocupied(position, sanity(x-1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x-1, y+1))
        # BLACK POWN
        elif position[key]['name'][1] == 'P' and position[key]['name'][0] == 'B' and position[key]['name'][0] != color:
          if ocupied(position, sanity(x+1, y-1)) == 'W':
            position[key]['moves'].append(sanity(x+1, y-1))
          if ocupied(position, sanity(x-1, y-1)) == 'W':
            position[key]['moves'].append(sanity(x-1, y-1))
        # WHITE ROOK
        elif position[key]['name'][1] == 'R' and position[key]['name'][0] == 'W':
          position = straight_move_test(position, key, x, y, 'B') 
        # BLACK ROOK
        elif position[key]['name'][1] == 'R' and position[key]['name'][0] == 'B':
          position = straight_move_test(position, key, x, y, 'W')
        # WHITE Bishop
        elif position[key]['name'][1] == 'B' and position[key]['name'][0] == 'W':
          position = incline_move_test(position, key, x, y, 'B') 
        # BLACK Bishop
        elif position[key]['name'][1] == 'B' and position[key]['name'][0] == 'B':
          position = incline_move_test(position, key, x, y, 'W')
        #WHITE KNIGHT
        elif position[key]['name'][0:3] == 'WKN':
          if not ocupied(position, sanity(x+2, y-1)) or ocupied(position, sanity(x+2, y-1)) == 'B':
            position[key]['moves'].append(sanity(x+2, y-1))
          if not ocupied(position, sanity(x+2, y+1)) or ocupied(position, sanity(x+2, y+1)) == 'B': 
            position[key]['moves'].append(sanity(x+2, y+1))
          if not ocupied(position, sanity(x-2, y+1)) or ocupied(position, sanity(x-2, y+1)) == 'B':
            position[key]['moves'].append(sanity(x-2, y+1))
          if not ocupied(position, sanity(x-2, y-1)) or ocupied(position, sanity(x-2, y-1)) == 'B':
            position[key]['moves'].append(sanity(x-2, y-1))
          if not ocupied(position, sanity(x-1, y+2)) or ocupied(position, sanity(x-1, y+2)) == 'B':
            position[key]['moves'].append(sanity(x-1, y+2))
          if not ocupied(position, sanity(x-1, y-2)) or ocupied(position, sanity(x-1, y-2)) == 'B':
            position[key]['moves'].append(sanity(x-1, y-2))
          if not ocupied(position, sanity(x+1, y+2)) or ocupied(position, sanity(x+1, y+2)) == 'B':
            position[key]['moves'].append(sanity(x+1, y+2))
          if not ocupied(position, sanity(x+1, y-2)) or ocupied(position, sanity(x+1, y-2)) == 'B':
            position[key]['moves'].append(sanity(x+1, y-2))
        #BLACK KNIGHT
        elif position[key]['name'][0:3] == 'BKN':
          if not ocupied(position, sanity(x+2, y-1)) or ocupied(position, sanity(x+2, y-1)) == 'W':
            position[key]['moves'].append(sanity(x+2, y-1))
          if not ocupied(position, sanity(x+2, y+1)) or ocupied(position, sanity(x+2, y+1)) == 'W': 
            position[key]['moves'].append(sanity(x+2, y+1))
          if not ocupied(position, sanity(x-2, y+1)) or ocupied(position, sanity(x-2, y+1)) == 'W':
            position[key]['moves'].append(sanity(x-2, y+1))
          if not ocupied(position, sanity(x-2, y-1)) or ocupied(position, sanity(x-2, y-1)) == 'W':
            position[key]['moves'].append(sanity(x-2, y-1))
          if not ocupied(position, sanity(x-1, y+2)) or ocupied(position, sanity(x-1, y+2)) == 'W':
            position[key]['moves'].append(sanity(x-1, y+2))
          if not ocupied(position, sanity(x-1, y-2)) or ocupied(position, sanity(x-1, y-2)) == 'W':
            position[key]['moves'].append(sanity(x-1, y-2))
          if not ocupied(position, sanity(x+1, y+2)) or ocupied(position, sanity(x+1, y+2)) == 'W':
            position[key]['moves'].append(sanity(x+1, y+2))
          if not ocupied(position, sanity(x+1, y-2)) or ocupied(position, sanity(x+1, y-2)) == 'W':
            position[key]['moves'].append(sanity(x+1, y-2))
        # WHITE QUEEN
        elif position[key]['name'][1] == 'Q' and position[key]['name'][0] == 'W':
          position = straight_move_test(position, key, x, y, 'B')
        # BLACK QUEEN
        elif position[key]['name'][1] == 'Q' and position[key]['name'][0] == 'B':
          position = straight_move_test(position, key, x, y, 'W') 
          position = incline_move_test(position, key, x, y, 'W')
        #WHITE KING
        elif position[key]['name'][0:3] == 'WKi':
          if not ocupied(position, sanity(x+1, y-1)) or ocupied(position, sanity(x+1, y-1)) == 'B':
            position[key]['moves'].append(sanity(x+1, y-1))
          if not ocupied(position, sanity(x+1, y+1)) or ocupied(position, sanity(x+1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x+1, y+1))
          if not ocupied(position, sanity(x+1, y)) or ocupied(position, sanity(x+1, y)) == 'B':
            position[key]['moves'].append(sanity(x+1, y))
          if not ocupied(position, sanity(x-1, y-1)) or ocupied(position, sanity(x-1, y-1)) == 'B':
            position[key]['moves'].append(sanity(x-1, y-1))
          if not ocupied(position, sanity(x-1, y+1)) or ocupied(position, sanity(x-1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x-1, y+1))
          if not ocupied(position, sanity(x-1, y)) or ocupied(position, sanity(x-1, y)) == 'B':
            position[key]['moves'].append(sanity(x-1, y))
          if not ocupied(position, sanity(x, y-1)) or ocupied(position, sanity(x, y-1)) == 'B':
            position[key]['moves'].append(sanity(x, y-1))
          if not ocupied(position, sanity(x, y+1)) or ocupied(position, sanity(x, y+1)) == 'B':
            position[key]['moves'].append(sanity(x, y+1))
        #BLACK KING
        elif position[key]['name'][0:3] == 'BKi':
          if not ocupied(position, sanity(x+1, y-1)) or ocupied(position, sanity(x+1, y-1)) == 'W':
            position[key]['moves'].append(sanity(x+1, y-1))
          if not ocupied(position, sanity(x+1, y+1)) or ocupied(position, sanity(x+1, y+1)) == 'W':
            position[key]['moves'].append(sanity(x+1, y+1))
          if not ocupied(position, sanity(x+1, y)) or ocupied(position, sanity(x+1, y)) == 'W':
            position[key]['moves'].append(sanity(x+1, y))
          if not ocupied(position, sanity(x-1, y-1)) or ocupied(position, sanity(x-1, y-1)) == 'W':
            position[key]['moves'].append(sanity(x-1, y-1))
          if not ocupied(position, sanity(x-1, y+1)) or ocupied(position, sanity(x-1, y+1)) == 'W':
            position[key]['moves'].append(sanity(x-1, y+1))
          if not ocupied(position, sanity(x-1, y)) or ocupied(position, sanity(x-1, y)) == 'W':
            position[key]['moves'].append(sanity(x-1, y))
          if not ocupied(position, sanity(x, y-1)) or ocupied(position, sanity(x, y-1)) == 'W':
            position[key]['moves'].append(sanity(x, y-1))
          if not ocupied(position, sanity(x, y+1)) or ocupied(position, sanity(x, y+1)) == 'W':
            position[key]['moves'].append(sanity(x, y+1))
  position = check_king(position)
  return position

def calculate_moves(position=start_position):
  position['WKing']['check'] = False
  position['BKing']['check'] = False
  for key in position:
    if position[key]['location'] != 'whiteHolder' and  position[key]['location'] != 'blackHolder':
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
      elif position[key]['name'][1] == 'P' and position[key]['name'][0] == 'B':
        if not ocupied(position, sanity(x, y-1)):
          position = save_king(position, key, sanity(x, y-1))
        if position[key]['notMoved'] and not ocupied(position, sanity(x, y-2)):
          position = save_king(position, key, sanity(x, y-2))
        if ocupied(position, sanity(x+1, y-1)) == 'W':
          position = save_king(position, key, sanity(x+1, y-1))
        if ocupied(position, sanity(x-1, y-1)) == 'W':
          position = save_king(position, key, sanity(x-1, y-1))
      # WHITE ROOK
      elif position[key]['name'][1] == 'R' and position[key]['name'][0] == 'W':
        position = straight_move(position, key, x, y, 'B') 
      # BLACK ROOK
      elif position[key]['name'][1] == 'R' and position[key]['name'][0] == 'B':
        position = straight_move(position, key, x, y, 'W')
      # WHITE Bishop
      elif position[key]['name'][1] == 'B' and position[key]['name'][0] == 'W':
        position = incline_move(position, key, x, y, 'B')
      # BLACK Bishop
      elif position[key]['name'][1] == 'B' and position[key]['name'][0] == 'B':
        position = incline_move(position, key, x, y, 'W')
      # WHITE KNIGHT
      elif position[key]['name'][0:3] == 'WKN':
        if not ocupied(position, sanity(x+2, y+1)) or ocupied(position, sanity(x+2, y+1)) == 'B':
          position = save_king(position, key, sanity(x+2, y+1))
        if not ocupied(position, sanity(x+2, y-1)) or ocupied(position, sanity(x+2, y-1)) == 'B':
          position = save_king(position, key, sanity(x+2, y-1))
        if not ocupied(position, sanity(x-2, y+1)) or ocupied(position, sanity(x-2, y+1)) == 'B':
          position = save_king(position, key, sanity(x-2, y+1))
        if not ocupied(position, sanity(x-2, y-1)) or ocupied(position, sanity(x-2, y-1)) == 'B':
          position = save_king(position, key, sanity(x-2, y-1))
        if not ocupied(position, sanity(x-1, y+2)) or ocupied(position, sanity(x-1, y+2)) == 'B':
          position = save_king(position, key, sanity(x-1, y+2))
        if not ocupied(position, sanity(x-1, y-2)) or ocupied(position, sanity(x-1, y-2)) == 'B':
          position = save_king(position, key, sanity(x-1, y-2))
        if not ocupied(position, sanity(x+1, y+2)) or ocupied(position, sanity(x+1, y+2)) == 'B':
          position = save_king(position, key, sanity(x+1, y+2))
        if not ocupied(position, sanity(x+1, y-2)) or ocupied(position, sanity(x+1, y-2)) == 'B':
          position = save_king(position, key, sanity(x+1, y-2))
      # BLACK KNIGHT
      elif position[key]['name'][0:3] == 'BKN':
        if not ocupied(position, sanity(x+2, y+1)) or ocupied(position, sanity(x+2, y+1)) == 'W':
          position = save_king(position, key, sanity(x+2, y+1))
        if not ocupied(position, sanity(x+2, y-1)) or ocupied(position, sanity(x+2, y-1)) == 'W':
          position = save_king(position, key, sanity(x+2, y-1))
        if not ocupied(position, sanity(x-2, y+1)) or ocupied(position, sanity(x-2, y+1)) == 'W':
          position = save_king(position, key, sanity(x-2, y+1))
        if not ocupied(position, sanity(x-2, y-1)) or ocupied(position, sanity(x-2, y-1)) == 'W':
          position = save_king(position, key, sanity(x-2, y-1))
        if not ocupied(position, sanity(x-1, y+2)) or ocupied(position, sanity(x-1, y+2)) == 'W':
          position = save_king(position, key, sanity(x-1, y+2))
        if not ocupied(position, sanity(x-1, y-2)) or ocupied(position, sanity(x-1, y-2)) == 'W':
          position = save_king(position, key, sanity(x-1, y-2))
        if not ocupied(position, sanity(x+1, y+2)) or ocupied(position, sanity(x+1, y+2)) == 'W':
          position = save_king(position, key, sanity(x+1, y+2))
        if not ocupied(position, sanity(x+1, y-2)) or ocupied(position, sanity(x+1, y-2)) == 'W':
          position = save_king(position, key, sanity(x+1, y-2))
      # WHITE QUEEN
      elif position[key]['name'][1] == 'Q' and position[key]['name'][0] == 'W':
        position = straight_move(position, key, x, y, 'B')
        position = incline_move(position, key, x, y, 'B')
      # BLACK QUEEN
      elif position[key]['name'][1] == 'Q' and position[key]['name'][0] == 'B':
        position = straight_move(position, key, x, y, 'W')
        position = incline_move(position, key, x, y, 'W')
      # BLACK KING
      elif position[key]['name'][0:3] == 'BKi':
        if not ocupied(position, sanity(x+1, y+1)) or ocupied(position, sanity(x+1, y+1)) == 'W':
          position = save_king(position, key, sanity(x+1, y+1))
        if not ocupied(position, sanity(x+1, y-1)) or ocupied(position, sanity(x+1, y-1)) == 'W':
          position = save_king(position, key, sanity(x+1, y-1))
        if not ocupied(position, sanity(x+1, y)) or ocupied(position, sanity(x+1, y)) == 'W':
          position = save_king(position, key, sanity(x+1, y))
        if not ocupied(position, sanity(x-1, y+1)) or ocupied(position, sanity(x-1, y+1)) == 'W':
          position = save_king(position, key, sanity(x-1, y+1))
        if not ocupied(position, sanity(x-1, y-1)) or ocupied(position, sanity(x-1, y-1)) == 'W':
          position = save_king(position, key, sanity(x-1, y-1))
        if not ocupied(position, sanity(x-1, y)) or ocupied(position, sanity(x-1, y)) == 'W':
          position = save_king(position, key, sanity(x-1, y))
        if not ocupied(position, sanity(x, y+1)) or ocupied(position, sanity(x, y+1)) == 'W':
          position = save_king(position, key, sanity(x, y+1))
        if not ocupied(position, sanity(x, y-1)) or ocupied(position, sanity(x, y-1)) == 'W':
          position = save_king(position, key, sanity(x, y-1))
      # WHITE KING
      elif position[key]['name'][0:3] == 'WKi':
        if not ocupied(position, sanity(x+1, y+1)) or ocupied(position, sanity(x+1, y+1)) == 'B':
          position = save_king(position, key, sanity(x+1, y+1))
        if not ocupied(position, sanity(x+1, y-1)) or ocupied(position, sanity(x+1, y-1)) == 'B':
          position = save_king(position, key, sanity(x+1, y-1))
        if not ocupied(position, sanity(x+1, y)) or ocupied(position, sanity(x+1, y)) == 'B':
          position = save_king(position, key, sanity(x+1, y))
        if not ocupied(position, sanity(x-1, y+1)) or ocupied(position, sanity(x-1, y+1)) == 'B':
          position = save_king(position, key, sanity(x-1, y+1))
        if not ocupied(position, sanity(x-1, y-1)) or ocupied(position, sanity(x-1, y-1)) == 'B':
          position = save_king(position, key, sanity(x-1, y-1))
        if not ocupied(position, sanity(x-1, y)) or ocupied(position, sanity(x-1, y)) == 'B':
          position = save_king(position, key, sanity(x-1, y))
        if not ocupied(position, sanity(x, y+1)) or ocupied(position, sanity(x, y+1)) == 'B':
          position = save_king(position, key, sanity(x, y+1))
        if not ocupied(position, sanity(x, y-1)) or ocupied(position, sanity(x, y-1)) == 'B':
          position = save_king(position, key, sanity(x, y-1))

  position = check_king(position)
  if position['WKing']['check'] or position['BKing']['check']:
    position = game_over(position)
  position = castling(position)
  return position

def attac(move, position):
  for key in position:
    if position[key]['location'] == move:
      if position[key]['color'] == 'white':
        return {'figure': position[key]['name'], 'holder':'whiteHolder'}
      else:
        return {'figure': position[key]['name'], 'holder':'blackHolder'}

def pawn_finder(position, loc, color):
  for key in position:
    if position[key]['location'] == loc and position[key]['name'][1] == 'P' and position[key]['color'] == color:
      return position[key]['name']
  return False

def en_passant(temp, figure, move_number):
  app.logger.info('en passant started')
  pawns = []
  for key in temp:
    if temp[key]['name'][1] == 'P':
      temp[key]['enPassant'] = False
      pawns.append(temp[key]['location'])
  x = int(temp[figure]['location'][0])
  y = int(temp[figure]['location'][1])
  if temp[figure]['name'][0] == 'W':
    if pawn_finder(temp, sanity(x-1, y), 'black'):
      name = pawn_finder(temp, sanity(x-1, y), 'black')
      temp[name]['enPassant'] = sanity(x,y-1)
      temp[name]['capture'] = sanity(x,y)  
      temp[name]['moves'].append(sanity(x,y-1))
    if pawn_finder(temp, sanity(x+1, y), 'black'):
      name = pawn_finder(temp, sanity(x+1, y), 'black')
      temp[name]['enPassant'] = sanity(x,y-1)
      temp[name]['capture'] = sanity(x,y)
      temp[name]['moves'].append(sanity(x,y-1))
  if temp[figure]['name'][0] == 'B':
    if pawn_finder(temp, sanity(x-1, y), 'white'):
      name = pawn_finder(temp, sanity(x-1, y), 'white')
      temp[name]['enPassant'] = sanity(x,y+1)
      temp[name]['capture'] = sanity(x,y)
      temp[name]['moves'].append(sanity(x,y+1))
    if pawn_finder(temp, sanity(x+1, y), 'white'):
      name = pawn_finder(temp, sanity(x+1, y), 'white')
      temp[name]['enPassant'] = sanity(x,y+1)
      temp[name]['capture'] = sanity(x,y)
      temp[name]['moves'].append(sanity(x,y+1))
  return temp
   
def time_master(time, white, black, move):
  now = datetime.datetime.utcnow()
  diff = now - time
  if move == 'white':
    white = white + diff.total_seconds()
  else:
    black = black + diff.total_seconds()
  return {'white': white, 'black': black}       

def move_length(loc, move):
  y = int(loc[1])
  moveY = int(move[1])
  if moveY - y == 2 or y - moveY == 2:
    return True
  return False

def promotion(temp, figure, move, wish):
  fig = temp[figure]
  if fig['name'][1] == 'P':
    if (fig['name'][0] == 'W' and move[1] == '7') or (fig['name'][0] == 'B' and move[1] == '0'):
      color = fig['color']
      location = fig['location']
      moves = fig['moves']
      temp.pop(figure, None)
      pic = wish[:2] + '.png'
      temp[wish] = {'name': wish, 'color': color, 'location': location, 'pic': pic, 'notMoved': False, 'moves': moves}
      return temp

def reffery(state, figure, move, promote):
  temp = state.position
  if promote:
    temp = promotion(temp, figure, move, promote)
    figure = promote
  if state.move == state.position[figure]['color']:
    if state.move == 'white':
      next_move = 'black'
    else:
      next_move = 'white'
    if move in state.position[figure]['moves']:
      if figure[1] == 'P' and state.position[figure]['enPassant'] == move:
        if state.position[figure]['enPassant'] in state.position[figure]['moves']:
          holder = attac(state.position[figure]['capture'], state.position)
          temp[holder['figure']]['location'] = holder['holder']
          temp[holder['figure']]['moves'] = []
      else:
        holder =  attac(move, state.position)
        if holder:
          temp[holder['figure']]['location'] = holder['holder']
          temp[holder['figure']]['moves'] = []
        elif figure[1] == 'K' and state.position[figure]['notMoved']:
          if move == '20':
            temp['WR1']['location'] = '30'
          elif move == '60':
            temp['WR2']['location'] = '50'
          elif move == '27':
            temp['BR1']['location'] = '37'
          elif move == '67':
            temp['BR2']['location'] = '57'
      move_temp = temp[figure]['location']
      temp[figure]['location'] = move
      temp[figure]['notMoved'] = False
      new_position = calculate_moves(temp)
      if temp[figure]['name'][1] == 'P' and move_temp and move_length(move_temp, move):
        new_position = en_passant(new_position, figure, state.move_number)
      time = time_master(state.date, state.white_timer, state.black_timer, state.move)
      return {'next_move': next_move, 'new_position': new_position, 'time': time}
  return False

def legal(state, figure, move):
  if state.move == state.position[figure]['color']:
    if move in state.position[figure]['moves']:
      return 1
    return 'Not legal move'
  return 'Not your move'
