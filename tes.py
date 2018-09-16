import random

# Read pions data from file external
def readFile(fileName, pions):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  dataSplited = []
  for x in data:
    dataSplited.append(x.split(' '))
  for y in dataSplited:
    createPion(y,pions)

# Create pions' data to dictionary
def createPion(dataPion,pions):
  amount = int(dataPion[2])
  listPoint = []

  x = random.randrange(8)
  y = random.randrange(8)
  listPoint.append((x,y))

  for i in range(0,amount):
    while( (x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
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
def printBoard():
  for i in range(0,8):
    for j in range(0,8):
        print("-",end="")
    print("\n")

pions = []
readFile('input.txt',pions)
printAllPion(pions)
printBoard()