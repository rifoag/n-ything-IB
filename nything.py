import random

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
    createpawn(row,pawns,listPoint) # Parse into desired format

# Create pawns' data to dictionary
def createpawn(datapawn,pawns,listPoint):
  amount = int(datapawn[2])

  x = random.randrange(8)
  y = random.randrange(8)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
    listPoint.append((x,y))
    pawns.append({'Type' : datapawn[1], 'color' : datapawn[0], 'row': x, 'col' : y})

# Print All pawns' data (Type, Color, Position)
def printAllpawn(pawns):
  for pawn in pawns:
    print("Type: ", pawn['Type'])
    print("Color: ", pawn['color'])
    print("PositionX: ", pawn['row'])
    print("PositionY: ", pawn['col'], "\n")

# Print chess board
def printBoard(pawns):
  for i in range(0,8):
    for j in range(0,8):
      isPawnExist = False
      for pawn in pawns:
        if (pawn['row']==i and pawn['col']==j):
          isPawnExist = True
          if (pawn['color'] == 'WHITE'):
            if (pawn['Type']=='QUEEN'):
              print('Q',end="")
            elif (pawn['Type']=='BISHOP'):
              print('B',end="")
            elif (pawn['Type']=='ROOK'):
              print('R',end="")
            elif (pawn['Type']=='KNIGHT'):
              print('K',end="")
          else:
            if (pawn['Type']=='QUEEN'):
              print('q',end="")
            elif (pawn['Type']=='BISHOP'):
              print('b',end="")
            elif (pawn['Type']=='ROOK'):
              print('r',end="")
            elif (pawn['Type']=='KNIGHT'):
              print('k',end="")
      if (not isPawnExist):
        print("-",end="")
    print("\n")

# Check whether the current pawn can attack the other pawn
def checkAttack(currPawn,dirPawn, pawns):
    if (currPawn['Type'] == "QUEEN"):
      return canAttackHorizontally(currPawn, dirPawn, pawns) or canAttackVertically(currPawn, dirPawn, pawns) or canAttackDiagonally(currPawn, dirPawn, pawns)
    if (currPawn['Type'] == "KNIGHT"):
      return (abs(currPawn["row"]-dirPawn["row"])==2 and abs(currPawn["col"]-dirPawn["col"])==1) or (abs(currPawn["row"]-dirPawn["row"])==1 and abs(currPawn["col"]-dirPawn["col"])==2)
    if (currPawn['Type'] == "BISHOP"):
      return canAttackDiagonally(currPawn, dirPawn, pawns)
    if (currPawn['Type'] == "ROOK"):
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
      # print("ROW : " + str(x))
      # print("COL : " + str(y))
      # check whether there's an obstacle in that cell
      for pawn in pawns:
        if (pawn["row"] == x and pawn["col"] == y):
          return False
      x += vgrad
      y += hgrad
    
    return True
  else:
    return False
  
# Fungsi Evaluasi jumlah penyerangan      
def Eval(pawns):
  sumAtk=0
  for pawn in pawns:
    for dir in pawns:
      if checkAttack(pawn,dir, pawns) and pawn!=dir:
        sumAtk+=1
  return sumAtk

pawns = []
readFile('input.txt',pawns)
printAllpawn(pawns)
printBoard(pawns)
print(Eval(pawns))