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
          if (pawn['color'] == 'WHITE'):
            if (pawn['type']=='QUEEN'):
              print('Q',end="")
            elif (pawn['type']=='BISHOP'):
              print('B',end="")
            elif (pawn['type']=='ROOK'):
              print('R',end="")
            elif (pawn['type']=='KNIGHT'):
              print('K',end="")
          else:
            if (pawn['type']=='QUEEN'):
              print('q',end="")
            elif (pawn['type']=='BISHOP'):
              print('b',end="")
            elif (pawn['type']=='ROOK'):
              print('r',end="")
            elif (pawn['type']=='KNIGHT'):
              print('k',end="")
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

# return all neighbour from a given state
def listAllNeighbour(pawns):
  stateList = []
  for idx, val in enumerate(pawns):
    for x in range(8):
      for y in range(8):
        if notOccupied(pawns, x, y):
          neighbourState = copy.deepcopy(pawns)
          neighbourState[idx]['row'] = x
          neighbourState[idx]['col'] = y
          stateList.append(neighbourState)            
  return stateList

pawns = []
readFile('input.txt',pawns)
printAllPawns(pawns)
printBoard(pawns)
print(evaluate(pawns))
allNeighbour = listAllNeighbour(pawns)
print("adam ganteng")