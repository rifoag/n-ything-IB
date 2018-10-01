import random

# Read state data from file external
def readFile(fileName, dataSplitted):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  for row in data:
    dataSplitted.append(row.split(' ')) # Parse input (per row) into a temporary array

# Generate state from the parsed input
def parseState(dataSplitted,pawnAmountBW):
  state=[]
  listPoint=[]
  pawnAmountBW['WHITE'] = 0
  pawnAmountBW['BLACK'] = 0
  for row in dataSplitted:
    createPawn(row, state, listPoint, pawnAmountBW) # Parse into desired format
  return state

# Push a pawn into a state
def createPawn(dataPawn, state, listPoint, pawnAmountBW):
  amount = int(dataPawn[2])
  pawnType = dataPawn[1]
  pawnColor = dataPawn[0]
  x = random.randrange(8)
  y = random.randrange(8)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
    listPoint.append((x,y))
    state.append({'type' : pawnType, 'color' : pawnColor, 'row': x, 'col' : y})
    pawnAmountBW[pawnColor] += 1 # Counter for each color of pawns

# Create list of State
def createListOfStates(dataSplitted,pawnAmountBW,numberOfStates):
  listOfStates=[]
  for i in range(0,numberOfStates):
    listOfStates.append(parseState(dataSplitted,pawnAmountBW))
  return listOfStates

# Print all state data (type, Color, Position)
def printStateInfo(state):
  for pawn in state:
    print("type: ", pawn['type'])
    print("Color: ", pawn['color'])
    print("PositionX: ", pawn['row'])
    print("PositionY: ", pawn['col'], "\n")

# Print chessboard
def printBoard(state):
  for i in range(0,8):
    for j in range(0,8):
      isPawnExist = False
      for pawn in state:
        if (pawn['row']==i and pawn['col']==j):
          isPawnExist = True
          if (pawn['color'] == 'BLACK'):
            if (pawn['type']=='QUEEN'):
              print('Q    ',end="")
            elif (pawn['type']=='BISHOP'):
              print('B    ',end="")
            elif (pawn['type']=='ROOK'):
              print('R    ',end="")
            elif (pawn['type']=='KNIGHT'):
              print('K    ',end="")
          else:
            if (pawn['type']=='QUEEN'):
              print('q    ',end="")
            elif (pawn['type']=='BISHOP'):
              print('b    ',end="")
            elif (pawn['type']=='ROOK'):
              print('r    ',end="")
            elif (pawn['type']=='KNIGHT'):
              print('k    ',end="")
      if (not isPawnExist):
        print("-    ",end="")
    print("\n")