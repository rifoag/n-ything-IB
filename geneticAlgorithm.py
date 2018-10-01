from evaluator import checkAttack, canAttackHorizontally, canAttackVertically, canAttackDiagonally, isEnemy, countAtack, notOccupied, evaluate, listAllNeighbour
from evaluator import decision
from operator import itemgetter
import random

# GA's main algorithm
def geneticAlgorithm(listOfStates, pawnAmountBW, populationAmount, limit):
  listOfStates = fitness(listOfStates, pawnAmountBW, populationAmount)
  generation = 0
  while ((evaluate(listOfStates[0], pawnAmountBW) != 0) and generation < limit): 
  # While the best state in the list haven't reach the best condition and it's not the last generation
    # Crossover
    numOfCrossovers = int(len(listOfStates)/2) # number of crossover to be done
    for j in range (0, numOfCrossovers):
      childrenStates = crossover(listOfStates[2*j], listOfStates[2*j+1])
      for state in childrenStates:
        if (decision(4)): # 4% chance of mutation
          mutation(state)
        listOfStates.append(state)
    # Evaluate by fitness rate
    listOfStates = fitness(listOfStates, pawnAmountBW, populationAmount) 
    generation += 1
  return listOfStates[0] # return the best state in the list
  
# crossover two state to generate 'child' states,
# a combination of one half of a state and another half from the other state
def crossover(state1, state2):
  if (len(state1) % 2 == 0):
    child1 = state1[0:int(len(state1)/2)] + state2[int(len(state1)/2):len(state2)]
    child2 = state2[0:int(len(state1)/2)] + state1[int(len(state1)/2):len(state2)]
  else:
    child1 = state1[0:(int(len(state1)/2)+1)] + state2[(int(len(state1)/2) + 1):len(state2)]
    child2 = state2[0:(int(len(state1)/2)+1)] + state1[(int(len(state1)/2) + 1):len(state2)]
  childStates = [child1, child2]
  return childStates

# Change a random pawn in the state to a random position
def mutation(state):
  i = random.randrange(0,len(state))
  x = random.randrange(0,8)
  y = random.randrange(0,8)
  while not notOccupied(state,x,y):
    x = random.randrange(0,8)
    y = random.randrange(0,8)
  state[i]['row'] = x
  state[i]['col'] = y

# Fitness Function
def fitness(listOfState, pawnAmountBW, populationAmount):
  result=[]
  listConnected=[]
  for idx, val in enumerate(listOfState):
    listConnected.append((idx,evaluate(val, pawnAmountBW)))
  listConnected = sorted(listConnected, key=itemgetter(1))
  for idx, val in listConnected:
    result.append(listOfState[idx])
  result = removeDuplicate(result)
  return result[:populationAmount] # return some 'best' states from the list 

# remove duplicate state in the list
def removeDuplicate(listOfStates):
  result = []
  for value in listOfStates:
    if value not in result:
      result.append(value)
  return result
