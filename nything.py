import random

# Read pions data from file external
def readFile(fileName, pions):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  dataSplited = []
  for row in data:
    dataSplited.append(row.split(' ')) # Parse input (per row) into a temporary array
  for row in dataSplited:
    createPion(row,pions) # Parse into desired format

# Create pions' data to dictionary
def createPion(dataPion,pions):
  amount = int(dataPion[2])
  listPoint = []

  x = random.randrange(4)
  y = random.randrange(4)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(4)
      y = random.randrange(4)
    listPoint.append((x,y))
    pions.append({'Type' : dataPion[1], 'color' : dataPion[0], 'row': x, 'col' : y})

# Print All Pions' data (Type, Color, Position)
def printAllPion(pions):
  for pion in pions:
    print("Type: ", pion['Type'])
    print("Color: ", pion['color'])
    print("PositionX: ", pion['row'])
    print("PositionY: ", pion['col'], "\n")

# Print chess board
def printBoard(pions):
  for i in range(0,8):
    for j in range(0,8):
      for pion in pions:
        if (pion['row']==i and pion['col']==j):
          if (pion['Type']=='QUEEN'):
            print('Q',end="")
          elif (pion['Type']=='BISHOP'):
            print('B',end="")
          elif (pion['Type']=='ROOK'):
            print('R',end="")
          elif (pion['Type']=='KNIGHT'):
            print('K',end="")
      else:
        print("-",end="")
    print("\n")

# Check if a pion can attack/can be attacked
def checkAttack(currPion,adjPion):
    currX = currPion["row"] # X coordinate current Pion
    currY = currPion["col"] # Y coordinate current Pion
    adjX = adjPion["row"]
    adjY = adjPion["col"]

    if (currPion['Type'] == "QUEEN"):
      return currX==adjX or currY==adjY or abs(currX - currY) == abs (adjX - adjY) 
    if (currPion['Type'] == "KNIGHT"):
      return (abs(currX-adjX)==2 and abs(currY-adjY)==1) or (abs(currX-adjX)==1 and abs(currY-adjY)==2)
    if (currPion['Type'] == "BISHOP"):
      return abs(currX - currY) == abs (adjX - adjY)
    if (currPion['Type'] == "ROOK"):
      return currX==adjX or currY==adjY

# fungsi Evaluasi jumlah penyerangan      
def Eval(pions):
  sumAtk=0
  for pion in pions:
    # temp = [x for x in pions if x!=pion]
    # for adj in temp:
    for adj in pions:
      if checkAttack(pion,adj) and pion!=adj:
        sumAtk+=1
  return sumAtk

pions = []
readFile('input.txt',pions)
printAllPion(pions)
printBoard(pions)
print(Eval(pions))