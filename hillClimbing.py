from evaluator import checkAttack, canAttackHorizontally, canAttackVertically, canAttackDiagonally, isEnemy, countAtack, notOccupied, evaluate, listAllNeighbour

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