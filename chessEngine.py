import copy
import datetime
occupied_old = []
start_position = {
  'WP8': {'name': 'WP8', 'color': 'white', 'location': '01', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP7': {'name': 'WP7', 'color': 'white', 'location': '11', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP6': {'name': 'WP6', 'color': 'white', 'location': '21', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP5': {'name': 'WP5', 'color': 'white', 'location': '31', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP4': {'name': 'WP4', 'color': 'white', 'location': '41', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP3': {'name': 'WP3', 'color': 'white', 'location': '51', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP2': {'name': 'WP2', 'color': 'white', 'location': '61', 'pic':'WP.png', 'notMoved': True, 'moves': []},
  'WP1': {'name': 'WP1', 'color': 'white', 'location': '71', 'pic':'WP.png','notMoved': True, 'moves': []},
  'BP8': {'name': 'BP8', 'color': 'black', 'location': '06', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP1': {'name': 'BP1', 'color': 'black', 'location': '16', 'pic':'BP.png', 'notMoved': 'true', 'moves': []},
  'BP2': {'name': 'BP2', 'color': 'black', 'location': '26', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP3': {'name': 'BP3', 'color': 'black', 'location': '36', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP4': {'name': 'BP4', 'color': 'black', 'location': '46', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP5': {'name': 'BP5', 'color': 'black', 'location': '56', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP6': {'name': 'BP6', 'color': 'black', 'location': '66', 'pic':'BP.png', 'notMoved': True, 'moves': []},
  'BP7': {'name': 'BP7', 'color': 'black', 'location': '76', 'pic':'BP.png', 'notMoved': True, 'moves': []},
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
        # 10 20 30
        long = True
        for key in position:
          if position[key]['location'] == '10' or position[key]['location'] == '20' or position[key]['location']  == '30':
            long = False
            break
        if long and save_castling(position, 'WKing', '20', 'WR1' , '30'):
          position['WKing']['long'] = True
          position['WKing']['moves'].append('20')
      if position['WR2']['notMoved']:
        # 50 60
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
        # 17 27 37
        long = True
        for key in position:
          if position[key]['location'] == '17' or position[key]['location'] == '27' or position[key]['location']  == '37':
            long = False
            break
        if long and save_castling(position, 'BKing', '27', 'BR1' , '37'):
          position['BKing']['long'] = True
          position['BKing']['moves'].append('27')
      if position['BR2']['notMoved']:
        # 57 67
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
  for key in position:
    if position[key]['name'][0] != color:
      if position[key]['location'] != 'whiteHolder' and  position[key]['location'] != 'blackHolder':
        position[key]['moves'] = []      
        x = int(position[key]['location'][0])
        y = int(position[key]['location'][1])
        # WHITE POWN
        if position[key]['name'][1] == 'P' and position[key]['name'][0] == 'W':
          if not ocupied(position, sanity(x, y+1)):
            position[key]['moves'].append(sanity(x, y+1))
          if position[key]['notMoved'] and not ocupied(position, sanity(x, y+2)):
            position[key]['moves'].append(sanity(x, y+2))
          if ocupied(position, sanity(x+1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x+1, y+1))
          if ocupied(position, sanity(x-1, y+1)) == 'B':
            position[key]['moves'].append(sanity(x-1, y+1))
        # BLACK POWN
        elif position[key]['name'][1] == 'P' and position[key]['name'][0] == 'B' and position[key]['name'][0] != color:
          if not ocupied(position, sanity(x, y-1)):
            position[key]['moves'].append(sanity(x, y-1))
          if position[key]['notMoved'] and not ocupied(position, sanity(x, y-2)):
            position[key]['moves'].append(sanity(x, y-2))
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
          position = incline_move_test(position, key, x, y, 'B')
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

def time_master(time, white, black, move):
  now = datetime.datetime.utcnow()
  diff = now - time
  if move == 'white':
    white = diff.total_seconds() - black
  else:
    black = diff.total_seconds() - white
  return {'white': white, 'black': black}

def en_passant(temp, figure, move, move_number):
  result = []
  pawns = []
  ocupied_old = []
  for key in temp:
    ocupied_old.append(temp[key]['location'])
    if temp[key]['name'][1] == 'P':
      pawns.append(temp[key]['location'])
  x = int(temp[figure]['location'][0])
  y = int(temp[figure]['location'][0])
  if temp[figure]['name'][0] == 'W':
    if sanity(x, y-1) not in ocupied_old:
      if sanity(x-1, y) in pawns:
        result.append((sanity(x, y-1), sanity(x-1, y)))
      if sanity(x+1, y) in pawns:
        result.append((sanity(x, y-1), sanity(x-1, y))) 
  if temp[figure]['name'][0] == 'B':
    if sanity(x, y+1) not in ocupied_old:
      if sanity(x-1, y) in pawns:
        result.append((sanity(x, y), sanity(x-1, y)))
      if sanity(x+1, y) in pawns:
        result.append((sanity(x, y-1), sanity(x-1, y)))
  if result:
    for n in result:
      for key in temp:
        if temp[key]['location']  == n[1]:
          if 'en_passant' in temp[key]:
            temp[key]['en_passant'].append((n[0], move_number))
            temp[key]['capture'].append(n[1])
          else:
            temp[key]['en_passant'] = [(n[0], move_number)]
            temp[key]['capture'] = [n[1]]
  return temp
          


def reffery(state, figure, move):
  if state.move == state.position[figure]['color']:
    if state.move == 'white':
      next_move = 'black'
    else:
      next_move = 'white'
    if move in state.position[figure]['moves']:
      temp = state.position
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
      temp[figure]['location'] = move
      if temp[figure]['name'][1] == 'P' and temp[figure]['notMoved']:
        temp = en_passant(temp, figure, move, state.move_number)
      temp[figure]['notMoved'] = False
      new_position = calculate_moves(temp)
      time = time_master(state.date, state.white_timer, state.black_timer, state.move)
      return {'next_move': next_move, 'new_position': new_position, 'time': time}
  return False