from evaluator import checkAttack, canAttackHorizontally, canAttackVertically, canAttackDiagonally, isEnemy, countAtack, notOccupied, evaluate, listAllNeighbour
from evaluator import decision
import random
from math import exp

# Simulated Annealing function, temperature decreasing by a given ratio over time
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
        isLocalMinim = False
      elif(temperature!=0):
        probability = int(exp(evaluate(neighbour,pawnAmountBW)-evalCurrent/temperature))
        if (decision(probability)):
          current = neighbour
          evalCurrent = evaluate(current,pawnAmountBW)
          isLocalMinim = False
    i+=1
    temperature *= decreaseRate/100
  return current