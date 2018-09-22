import random
import copy

# Read pawns data from file external
def readFile(fileName, pawns):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  dataSplited = []
  listPoint = []
  for row in data:
    dataSplited.append(row.split(' ')) # Parse input (per row) into a temporary array
  for row in dataSplited:
    createPawn(row,pawns,listPoint) # Parse into desired format

# Create pawns' data to dictionary
def createPawn(datapawn,pawns,listPoint):
  amount = int(datapawn[2])

  x = random.randrange(8)
  y = random.randrange(8)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
    listPoint.append((x,y))
    pawns.append({'type' : datapawn[1], 'color' : datapawn[0], 'row': x, 'col' : y})

# Print all pawns data (type, Color, Position)
def printAllPawns(pawns):
  for pawn in pawns:
    print("type: ", pawn['type'])
    print("Color: ", pawn['color'])
    print("PositionX: ", pawn['row'])
    print("PositionY: ", pawn['col'], "\n")

# Print chessboard
def printBoard(pawns):
  for i in range(0,8):
    for j in range(0,8):
      isPawnExist = False
      for pawn in pawns:
        if (pawn['row']==i and pawn['col']==j):
          isPawnExist = True
          if (pawn['type']=='QUEEN'):
            print('Q',end="")
          elif (pawn['type']=='BISHOP'):
            print('B',end="")
          elif (pawn['type']=='ROOK'):
            print('R',end="")
          elif (pawn['type']=='KNIGHT'):
            print('K',end="")
      if (not isPawnExist):
        print("-",end="")
    print("\n")

# Check whether the current pawn can attack the other pawn
def checkAttack(currPawn,dirPawn, pawns):
    if (currPawn['type'] == "QUEEN"):
      return canAttackHorizontally(currPawn, dirPawn, pawns) or canAttackVertically(currPawn, dirPawn, pawns) or canAttackDiagonally(currPawn, dirPawn, pawns)
    if (currPawn['type'] == "KNIGHT"):
      return (abs(currPawn["row"]-dirPawn["row"])==2 and abs(currPawn["col"]-dirPawn["col"])==1) or (abs(currPawn["row"]-dirPawn["row"])==1 and abs(currPawn["col"]-dirPawn["col"])==2)
    if (currPawn['type'] == "BISHOP"):
      return canAttackDiagonally(currPawn, dirPawn, pawns)
    if (currPawn['type'] == "ROOK"):
      return canAttackHorizontally(currPawn, dirPawn, pawns) or canAttackVertically(currPawn, dirPawn, pawns)

# Check whether the current pawn can attack the other pawn (horizontally)
def canAttackHorizontally(currPawn,dirPawn, pawns):
  if (currPawn["row"] == dirPawn["row"]):
    # Check whether there's another pawn between them
    for pawn in pawns: 
      if (pawn["row"] == currPawn["row"]):
        if (currPawn["col"] < dirPawn["col"]) and (currPawn["col"] < pawn["col"]) and (pawn["col"] < dirPawn["col"]):
          return False
        if (currPawn["col"] > dirPawn["col"]) and (currPawn["col"] > pawn["col"]) and (pawn["col"] > dirPawn["col"]):
          return False
    return True
  else:
    return False

# Check whether the current pawn can attack the other pawn (vertically)
def canAttackVertically(currPawn, dirPawn, pawns):
  if (currPawn["col"] == dirPawn["col"]):
    # Check whether there's another pawn between them
    for pawn in pawns: 
      if (pawn["col"] == currPawn["col"]):
        if (currPawn["row"] < dirPawn["row"]) and (currPawn["row"] < pawn["row"]) and (pawn["row"] < dirPawn["row"]):
          return False
        if (currPawn["row"] > dirPawn["row"]) and (currPawn["row"] > pawn["row"]) and (pawn["row"] > dirPawn["row"]):
          return False
    return True
  else:
    return False

# Check whether the current pawn can attack the other pawn (diagonally)
def canAttackDiagonally(currPawn, dirPawn, pawns):
  if (abs(currPawn["col"] - dirPawn["col"]) == abs(currPawn["row"] - dirPawn["row"])): # both pawns is in the same diagonal
    hgrad = 1 if (currPawn["col"] < dirPawn["col"]) else -1
    vgrad = 1 if (currPawn["row"] < dirPawn["row"]) else -1
  
    x = currPawn["row"] + vgrad # Row iterator
    y = currPawn["col"] + hgrad # Col iterator

    while (x != dirPawn["row"] and y != dirPawn["col"] and x > 0 and y > 0):
      # check whether there's an obstacle in that cell
      for pawn in pawns:
        if (pawn["row"] == x and pawn["col"] == y):
          return False
      x += vgrad
      y += hgrad
    
    return True
  else:
    return False

# Count how many chess piece that can attack another piece
def evaluate(pawns):
  sumAtk=0
  for pawn in pawns:
    for dir in pawns:
      if checkAttack(pawn,dir, pawns) and pawn!=dir:
        sumAtk+=1
  return sumAtk

# check if a cell is not occupied by a pawn
def notOccupied(pawns, x, y):
  for pawn in pawns:
    if (pawn['row'] == x and pawn['col'] == y):
      return False
  return True

# return all position that may be reached by the current pawn, given the current state
def eligibleMoves(pawns, pawn):
  pos = [] # all point that can be reached by the pawn
  x = pawn['row']
  y = pawn['col']

  if (pawn['type'] == 'ROOK' or pawn['type'] == 'QUEEN'):
    for i in range(8):
      if notOccupied(pawns, x, i):
        pos.append({'row': x , 'col': i})
      if notOccupied(pawns, i, y):
        pos.append({'row': i , 'col': y})
  elif (pawn['type'] == 'BISHOP' or pawn['type'] == 'QUEEN'):
      # quad 1
      h = 1 # horizontal movement
      v = 1 # vertical movement
      while (x + h < 8 and y + v < 8):
        if notOccupied(pawns, x + h, y + v):
          pos.append({'row': x+h , 'col': y+v})
          h += 1
          v += 1
      # quad 2
      h = -1
      v = 1
      while (x + h >= 0 and y + v < 8):
        if notOccupied(pawns, x + h, y + v):
          pos.append({'row': x+h , 'col': y+v})
          h -= 1
          v += 1
      # quad 3 
      h = -1
      v = -1
      while (x + h >= 0 and y + v >= 0):
        if notOccupied(pawns, x + h, y + v):
          pos.append({'row': x+h , 'col': y+v})
          h -= 1
          v -= 1
      # quad 4
      h = 1
      v = -1
      while (x + h < 8 and y + v >= 0):
        if notOccupied(pawns, x + h, y + v):
          pos.append({'row': x+h , 'col': y+v})
          h += 1
          v -= 1
  elif (pawn['type'] == 'KNIGHT'):
    for i in range(8): # check all 8 possible moves of a knight 
      h = [1,1,2,2,-1,-1,-2,-2]
      v = [2,-2,1,-1,2,-2,1,-1]
      for i in range(8):
        if ((x + h[i] >= 0 and x + h[i] < 8 and y + v[i] >= 0 and y + v[i] < 8) and (notOccupied(pawns, x + h[i], y + v[i]))):
          pos.append({'row': x+h[i] , 'col': y+v[i]})
  return pos

# return all neighbour from a given state
def listAllNeighbour(pawns):
  stateList = []
  for idx, val in enumerate(pawns):
    positions = eligibleMoves(pawns, val) # get all position that may be reached by the current pawn
    for pos in positions:
      neighbourState = copy.deepcopy(pawns)
      neighbourState[idx]['row'] = pos['row']
      neighbourState[idx]['col'] = pos['col']
      stateList.append(neighbourState)
  return stateList

pawns = []
readFile('input.txt',pawns)
printAllPawns(pawns)
printBoard(pawns)
print(evaluate(pawns))