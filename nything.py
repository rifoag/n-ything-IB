import random
import copy
from math import exp
from operator import itemgetter

# Read pawns data from file external
def readFile(fileName, dataSplitted):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  for row in data:
    dataSplitted.append(row.split(' ')) # Parse input (per row) into a temporary array

# membuat state dari data
def parsePawns(dataSplitted,numberOfPawns):
  pawns=[]
  listPoint=[]
  for row in dataSplitted:
    createPawn(row, pawns, listPoint, numberOfPawns) # Parse into desired format
  return pawns

# membuat list of state dari data
def createListOfPawns(dataSplitted,numberOfPawns,JumlahPawns):
  listOfPawns=[]
  for i in range(0,JumlahPawns):
    listOfPawns.append(parsePawns(dataSplitted,numberOfPawns))
  return listOfPawns
# Menu
def menuInit(pawns, numberOfPawns):
  fileName = input('Enter file name : ')
  dataSplitted=[]
  readFile(fileName, dataSplitted)
  pawns=parsePawns(dataSplitted,numberOfPawns)
  print("Pawns Data : ")
  printAllPawns(pawns)
  print("Board First Condition : ")
  printBoard(pawns)
  print("Choose Algorithm By Input The Number :")
  print("1. Hill Climbing")
  print("2. Simulted Annealing")
  print("3. Genetic Algorithm")
  chosenAlgo = int(input("Choose : "))
  while (chosenAlgo > 3 or chosenAlgo < 1):
    print("Chose The Correct Number Please...")
    chosenAlgo = int(input("Choose : "))
  if (chosenAlgo == 1):
    hasil = hillClimbing(pawns,numberOfPawns)
    print(hasil)
    print(evaluate(hasil,numberOfPawns))
  elif (chosenAlgo == 2):
    temperature = int(input('Temperature: '))
    decreaseRate = int(input('Decrease Rate: '))
    iteration = int(input('Maximum Iteration: '))
    hasil = simulatedAnnealing2(pawns,numberOfPawns,temperature,decreaseRate,iteration)
    print(hasil)
    print(evaluate(hasil,numberOfPawns))
  elif (chosenAlgo == 3):
    jumlahPopulasi= int(input('Sum Of Population: '))
    limit = int(input('Maximum generation: '))
    listOfPawns = createListOfPawns(dataSplitted,numberOfPawns,jumlahPopulasi)
    hasil = geneticAlgoritm(listOfPawns,numberOfPawns,jumlahPopulasi,limit)
    print(len(hasil))
    for state in hasil:
      print("state: ")
      print(state)
      print(evaluate(state,numberOfPawns))

# Create pawns' data to dictionary
def createPawn(datapawn, pawns, listPoint, numberOfPawns):
  amount = int(datapawn[2])
  x = random.randrange(8)
  y = random.randrange(8)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
    listPoint.append((x,y))
    pawns.append({'type' : datapawn[1], 'color' : datapawn[0], 'row': x, 'col' : y})
    numberOfPawns[datapawn[0]] += 1

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

# Check if two chess piece is an enemy
def isEnemy(pawn, dirPawn):
  if (pawn['color'] != dirPawn['color']):
    return True
  else:
    return False

# Count how many chess piece that can attack another piece
def evaluate(pawns, numberOfPawns):
  canAttackEnemy = 0
  canAttackFriend = 0
  for pawn in pawns:
    for dirPawn in pawns:
      if checkAttack(pawn, dirPawn, pawns) and pawn!=dirPawn:
        if (isEnemy(pawn, dirPawn)):
          canAttackEnemy += 1
        else: # the other piece is not an enemy
          canAttackFriend += 1
  if(numberOfPawns['BLACK'] == 0 or numberOfPawns['WHITE'] == 0):
    return canAttackFriend
  else:
    return canAttackFriend + (2*numberOfPawns['BLACK']*numberOfPawns['WHITE'] - canAttackEnemy)

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

# hill climbing function without color constraint
def hillClimbing(initState, numberOfPawns):
  current = initState
  evalCurrent = evaluate(current, numberOfPawns)
  isLocalMinim = False
  while (evalCurrent != 0 and not isLocalMinim):
    isLocalMinim = True
    AllNeighbour = listAllNeighbour(current)
    for neighbour in AllNeighbour:
      if (evalCurrent > evaluate(neighbour, numberOfPawns)):
        isLocalMinim = False
        current = neighbour
        evalCurrent = evaluate(neighbour, numberOfPawns)
  return current

def decision(probability):
  return random.randrange(100) < probability

# Simulated Annealing function, temperature decreasing by ratio
def simulatedAnnealing(initState,numberOfPawns,temperature,decreaseRate,iteration):
  current = initState
  evalCurrent = evaluate(current,numberOfPawns)
  i = 0
  isOver = False
  while (evalCurrent != 0 and i < iteration and not isOver):
    isOver = True
    AllNeighbour = listAllNeighbour(current)
    for neighbour in AllNeighbour:
      if (evalCurrent > evaluate(neighbour,numberOfPawns)):
        current = neighbour
        evalCurrent = evaluate(current,numberOfPawns)
        i+=1
        temperature *= decreaseRate/100.00
        isOver = False
      elif(temperature!=0):
        probability = int(exp(evaluate(neighbour,numberOfPawns)-evalCurrent/temperature))
        if (decision(probability)):
          current = neighbour
          evalCurrent = evaluate(current,numberOfPawns)
          i+=1
          temperature *= decreaseRate/100
          isOver = False
  return current

def simulatedAnnealing2(initState,numberOfPawns,temperature,decreaseRate,iteration):
  current = initState
  evalCurrent = evaluate(current,numberOfPawns)
  i = 0
  while (evalCurrent != 0 and i < iteration):
    neighbour = randomMove(current)
    if (evalCurrent > evaluate(neighbour,numberOfPawns)):
      current = neighbour
      evalCurrent = evaluate(current,numberOfPawns)
      temperature *= decreaseRate/100.00
    elif(temperature!=0):
      probability = int(exp(evaluate(neighbour,numberOfPawns)-evalCurrent/temperature))
      if (decision(probability)):
        current = neighbour
        evalCurrent = evaluate(current,numberOfPawns)
        temperature *= decreaseRate/100
    i+=1
  return current

#Metode penyelesaian menggunakan genetic algorithm
def geneticAlgoritm(listOfPawns,numberOfPawns,jumlahPopulasi,limit):
  listOfPawns = fitness(listOfPawns,numberOfPawns,jumlahPopulasi)
  i = 0
  while ( (evaluate(listOfPawns[0],numberOfPawns) != 0) and i < limit):
    jumlahCrossOver = int(len(listOfPawns)/2)
    for j in range (0,jumlahCrossOver):
      anakAnak = crossOver(listOfPawns[2*j],listOfPawns[2*j+1])
      for anak in anakAnak:
        mutation(anak)
        listOfPawns.append(anak)
    listOfPawns = fitness(listOfPawns,numberOfPawns,jumlahPopulasi)
    i+=1
  return listOfPawns
  
# crossover setengah dari anak
def crossOver(state1, state2):
  # anakAnak = []
  # anak1 = []
  # anak2 = []
  if (len(state1) % 2 == 0):
    # anak1.append(state1[0:int(len(state1)/2)])
    # anak1.append(state2[(int(len(state1)/2) + 1):len(state2)])
    # anak2.append(state2[0:int(len(state1)/2)])
    # anak2.append(state1[(int(len(state1)/2) + 1):len(state2)])
    anak1 = state1[0:int(len(state1)/2)] + state2[int(len(state1)/2):len(state2)]
    anak2 = state2[0:int(len(state1)/2)] + state1[int(len(state1)/2):len(state2)]

  else:
    # anak1.append(state1[0:(int(len(state1)/2)+1)])
    # anak1.append(state2[(int(len(state1)/2) + 2):len(state2)])
    # anak2.append(state2[0:(int(len(state1)/2)+1)])
    # anak2.append(state1[(int(len(state1)/2) + 2):len(state2)])
    anak1 = state1[0:(int(len(state1)/2)+1)] + state2[(int(len(state1)/2) + 1):len(state2)]
    anak2 = state2[0:(int(len(state1)/2)+1)] + state1[(int(len(state1)/2) + 1):len(state2)]
  anakAnak = [anak1, anak2]
  return anakAnak

# Mengganti posisi pion secara random ke posisi random
def mutation(state):
  i = random.randrange(0,len(state))
  x = random.randrange(0,8)
  y = random.randrange(0,8)
  while not notOccupied(state,x,y):
    x = random.randrange(0,8)
    y = random.randrange(0,8)
  state[i]['row'] = x
  state[i]['col'] = y

#Fitness Function
def fitness(listOfState, numberOfPawns, jumlahPopulasi):
  hasil=[]
  listConnected=[]
  for idx,val in enumerate(listOfState):
    listConnected.append((idx,evaluate(val,numberOfPawns)))
  listConnected = sorted(listConnected,key=itemgetter(1))
  for idx,val in listConnected:
    hasil.append(listOfState[idx])
  hasil = removeDuplicate(hasil)
  return hasil[:jumlahPopulasi]

# remove Duplicate list
def removeDuplicate(listState):
  hasil = []
  for value in listState:
    if value not in hasil:
      hasil.append(value)
  return hasil

# random move
def randomMove(state):
  neighbour = state
  i = random.randrange(0,len(state))
  x = random.randrange(0,8)
  y = random.randrange(0,8)
  while not notOccupied(state,x,y):
    x = random.randrange(0,8)
    y = random.randrange(0,8)
  neighbour[i]['row'] = x
  neighbour[i]['col'] = y
  return neighbour 

pawns=[]
numberOfPawns = {}
numberOfPawns['WHITE'] = 0
numberOfPawns['BLACK'] = 0
dataSplitted = []
menuInit(pawns,numberOfPawns)