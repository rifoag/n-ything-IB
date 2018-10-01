import copy
import random

# given a probability, choose whether to take the decision or not
def decision(probability):
  return random.randrange(100) < probability

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
        elif (currPawn["col"] > dirPawn["col"]) and (currPawn["col"] > pawn["col"]) and (pawn["col"] > dirPawn["col"]):
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
        elif (currPawn["row"] > dirPawn["row"]) and (currPawn["row"] > pawn["row"]) and (pawn["row"] > dirPawn["row"]):
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

def countAtack(state):
  canAttackEnemy = 0
  canAttackFriend = 0
  for pawn in state:
    for dirPawn in state:
      if checkAttack(pawn, dirPawn, state) and pawn!=dirPawn:
        if (isEnemy(pawn, dirPawn)):
          canAttackEnemy += 1
        else: # the other piece is not an enemy
          canAttackFriend += 1
  count = {'friend': canAttackFriend, 'enemy': canAttackEnemy}
  return count

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