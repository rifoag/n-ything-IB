import random
import copy
from math import exp
from operator import itemgetter

# Read state data from file external
def readFile(fileName, dataSplitted):
  file = open(fileName, 'r')
  data = file.read()
  data = data.split('\n') # List of entire data
  for row in data:
    dataSplitted.append(row.split(' ')) # Parse input (per row) into a temporary array

# membuat state dari data
def parseState(dataSplitted,pawnAmountBW):
  state=[]
  listPoint=[]
  for row in dataSplitted:
    createPawn(row, state, listPoint, pawnAmountBW) # Parse into desired format
  return state

# membuat list of state dari data
def createListOfState(dataSplitted,pawnAmountBW,jumlahState):
  listOfState=[]
  for i in range(0,jumlahState):
    listOfState.append(parseState(dataSplitted,pawnAmountBW))
  return listOfState

# Menu
def menuInit():
  fileName = input('Enter file name : ')
  dataSplitted=[]
  readFile(fileName, dataSplitted)
  pawnAmountBW = {}
  pawnAmountBW['WHITE'] = 0
  pawnAmountBW['BLACK'] = 0
  state=parseState(dataSplitted,pawnAmountBW)
  print("State Data : ")
  printAllState(state)
  print("Board First Condition : ")
  printBoard(state)
  print("Choose Algorithm By Input The Number :")
  print("1. Hill Climbing")
  print("2. Simulted Annealing")
  print("3. Genetic Algorithm")
  chosenAlgo = int(input("Choose : "))
  while (chosenAlgo > 3 or chosenAlgo < 1):
    print("Chose The Correct Number Please...")
    chosenAlgo = int(input("Choose : "))
  if (chosenAlgo == 1):
    hasil = hillClimbing(state,pawnAmountBW)
  elif (chosenAlgo == 2):
    temperature = int(input('Temperature: '))
    decreaseRate = int(input('Decrease Rate: '))
    iteration = int(input('Maximum Iteration: '))
    hasil = simulatedAnnealing(state,pawnAmountBW,temperature,decreaseRate,iteration)
  elif (chosenAlgo == 3):
    jumlahPopulasi= int(input('Sum Of Population: '))
    limit = int(input('Maximum generation: '))
    listOfstate = createListOfState(dataSplitted,pawnAmountBW,jumlahPopulasi)
    hasil = geneticAlgoritm(listOfstate,pawnAmountBW,jumlahPopulasi,limit)
  printBoard(hasil)
  print(evaluate(hasil,pawnAmountBW))

# Create state' data to dictionary
def createPawn(dataPawn, state, listPoint, pawnAmountBW):
  amount = int(dataPawn[2])
  x = random.randrange(8)
  y = random.randrange(8)

  for i in range(0,amount):
    while((x,y) in listPoint):
      x = random.randrange(8)
      y = random.randrange(8)
    listPoint.append((x,y))
    state.append({'type' : dataPawn[1], 'color' : dataPawn[0], 'row': x, 'col' : y})
    pawnAmountBW[dataPawn[0]] += 1

# Print all state data (type, Color, Position)
def printAllState(state):
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

# Check whether the current pawn can attack the other pawn
def checkAttack(currPawn,dirPawn, state):
    if (currPawn['type'] == "QUEEN"):
      return canAttackHorizontally(currPawn, dirPawn, state) or canAttackVertically(currPawn, dirPawn, state) or canAttackDiagonally(currPawn, dirPawn, state)
    if (currPawn['type'] == "KNIGHT"):
      return (abs(currPawn["row"]-dirPawn["row"])==2 and abs(currPawn["col"]-dirPawn["col"])==1) or (abs(currPawn["row"]-dirPawn["row"])==1 and abs(currPawn["col"]-dirPawn["col"])==2)
    if (currPawn['type'] == "BISHOP"):
      return canAttackDiagonally(currPawn, dirPawn, state)
    if (currPawn['type'] == "ROOK"):
      return canAttackHorizontally(currPawn, dirPawn, state) or canAttackVertically(currPawn, dirPawn, state)

# Check whether the current pawn can attack the other pawn (horizontally)
def canAttackHorizontally(currPawn,dirPawn, state):
  if (currPawn["row"] == dirPawn["row"]):
    # Check whether there's another pawn between them
    for pawn in state: 
      if (pawn["row"] == currPawn["row"]):
        if (currPawn["col"] < dirPawn["col"]) and (currPawn["col"] < pawn["col"]) and (pawn["col"] < dirPawn["col"]):
          return False
        if (currPawn["col"] > dirPawn["col"]) and (currPawn["col"] > pawn["col"]) and (pawn["col"] > dirPawn["col"]):
          return False
    return True
  else:
    return False

# Check whether the current pawn can attack the other pawn (vertically)
def canAttackVertically(currPawn, dirPawn, state):
  if (currPawn["col"] == dirPawn["col"]):
    # Check whether there's another pawn between them
    for pawn in state: 
      if (pawn["col"] == currPawn["col"]):
        if (currPawn["row"] < dirPawn["row"]) and (currPawn["row"] < pawn["row"]) and (pawn["row"] < dirPawn["row"]):
          return False
        if (currPawn["row"] > dirPawn["row"]) and (currPawn["row"] > pawn["row"]) and (pawn["row"] > dirPawn["row"]):
          return False
    return True
  else:
    return False

# Check whether the current pawn can attack the other pawn (diagonally)
def canAttackDiagonally(currPawn, dirPawn, state):
  if (abs(currPawn["col"] - dirPawn["col"]) == abs(currPawn["row"] - dirPawn["row"])): # both state is in the same diagonal
    hgrad = 1 if (currPawn["col"] < dirPawn["col"]) else -1
    vgrad = 1 if (currPawn["row"] < dirPawn["row"]) else -1
  
    x = currPawn["row"] + vgrad # Row iterator
    y = currPawn["col"] + hgrad # Col iterator

    while (x != dirPawn["row"] and y != dirPawn["col"] and x > 0 and y > 0):
      # check whether there's an obstacle in that cell
      for pawn in state:
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
def evaluate(state, pawnAmountBW):
  canAttackEnemy = 0
  canAttackFriend = 0
  for pawn in state:
    for dirPawn in state:
      if checkAttack(pawn, dirPawn, state) and pawn!=dirPawn:
        if (isEnemy(pawn, dirPawn)):
          canAttackEnemy += 1
        else: # the other piece is not an enemy
          canAttackFriend += 1
  if(pawnAmountBW['BLACK'] == 0 or pawnAmountBW['WHITE'] == 0):
    return canAttackFriend
  else:
    return canAttackFriend + (2*pawnAmountBW['BLACK']*pawnAmountBW['WHITE'] - canAttackEnemy)

# check if a cell is not occupied by a pawn
def notOccupied(state, x, y):
  for pawn in state:
    if (pawn['row'] == x and pawn['col'] == y):
      return False
  return True

# return all neighbour from a given state
def listAllNeighbour(state):
  stateList = []
  for idx, val in enumerate(state):
    for x in range(8):
      for y in range(8):
        if notOccupied(state, x, y):
          neighbourState = copy.deepcopy(state)
          neighbourState[idx]['row'] = x
          neighbourState[idx]['col'] = y
          stateList.append(neighbourState)            
  return stateList

# hill climbing function without color constraint
def hillClimbing(initState, pawnAmountBW):
  current = initState
  evalCurrent = evaluate(current, pawnAmountBW)
  isLocalMinim = False
  while (evalCurrent != 0 and not isLocalMinim):
    isLocalMinim = True
    AllNeighbour = listAllNeighbour(current)
    for neighbour in AllNeighbour:
      if (evalCurrent > evaluate(neighbour, pawnAmountBW)):
        isLocalMinim = False
        current = neighbour
        evalCurrent = evaluate(neighbour, pawnAmountBW)
  return current

def decision(probability):
  return random.randrange(100) < probability

# Simulated Annealing function, temperature decreasing by ratio
def simulatedAnnealing(initState,pawnAmountBW,temperature,decreaseRate,iteration):
  current = initState
  evalCurrent = evaluate(current,pawnAmountBW)
  i = 0
  isLocalMinim = False
  while (evalCurrent != 0 and i < iteration and not isLocalMinim):
    isLocalMinim = True
    AllNeighbour = listAllNeighbour(current)
    for neighbour in AllNeighbour:
      if (evalCurrent > evaluate(neighbour,pawnAmountBW)):
        current = neighbour
        evalCurrent = evaluate(current,pawnAmountBW)
        i+=1
        temperature *= decreaseRate/100.00
        isLocalMinim = False
      elif(temperature!=0):
        probability = int(exp(evaluate(neighbour,pawnAmountBW)-evalCurrent/temperature))
        if (decision(probability)):
          current = neighbour
          evalCurrent = evaluate(current,pawnAmountBW)
          i+=1
          temperature *= decreaseRate/100
          isLocalMinim = False
  return current

#Metode penyelesaian menggunakan genetic algorithm
def geneticAlgoritm(listOfstate,pawnAmountBW,jumlahPopulasi,limit):
  listOfstate = fitness(listOfstate,pawnAmountBW,jumlahPopulasi)
  i = 0
  while ( (evaluate(listOfstate[0],pawnAmountBW) != 0) and i < limit):
    jumlahCrossOver = int(len(listOfstate)/2)
    for j in range (0,jumlahCrossOver):
      anakAnak = crossOver(listOfstate[2*j],listOfstate[2*j+1])
      for anak in anakAnak:
        if (decision(2)):
          mutation(anak)
        listOfstate.append(anak)
    listOfstate = fitness(listOfstate,pawnAmountBW,jumlahPopulasi)
    i+=1
  return listOfstate[0]
  
# crossover setengah dari anak
def crossOver(state1, state2):
  if (len(state1) % 2 == 0):
    anak1 = state1[0:int(len(state1)/2)] + state2[int(len(state1)/2):len(state2)]
    anak2 = state2[0:int(len(state1)/2)] + state1[int(len(state1)/2):len(state2)]

  else:
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
def fitness(listOfState, pawnAmountBW, jumlahPopulasi):
  hasil=[]
  listConnected=[]
  for idx,val in enumerate(listOfState):
    listConnected.append((idx,evaluate(val,pawnAmountBW)))
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

menuInit()