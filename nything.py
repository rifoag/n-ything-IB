# Import program's utility module
from utilities import readFile, parseState, createPawn, createListOfStates, printStateInfo, printBoard

# Import program algorithm
from evaluator import checkAttack, canAttackHorizontally, canAttackVertically, canAttackDiagonally, isEnemy, countAtack, notOccupied, evaluate, listAllNeighbour
from hillClimbing import hillClimbing
from simulatedAnnealing import simulatedAnnealing
from geneticAlgorithm import geneticAlgorithm

# Program's main menu
def main():
  fileName = input('Enter file name : ')
  # Used variables
  pawnAmountBW = {'WHITE': 0, 'BLACK': 0} # number of pawns for each side
  dataSplitted = []
  readFile(fileName, dataSplitted) # parse user's input into array

  # Algorithms option
  print("Choose Algorithm By Input The Number :")
  print("1. Hill Climbing")
  print("2. Simulated Annealing")
  print("3. Genetic Algorithm")
  chosenAlgo = int(input("Choose : "))
  while (chosenAlgo > 3 or chosenAlgo < 1):
    print("Choose The Correct Number Please...")
    chosenAlgo = int(input("Choose : "))

  # Execute the chosen algorithm
  if (chosenAlgo == 1):
    state = parseState(dataSplitted, pawnAmountBW) # generate an initial state
    result = hillClimbing(state, pawnAmountBW)
  elif (chosenAlgo == 2):
    temperature = int(input('Temperature: '))
    decreaseRate = int(input('Decrease Rate: '))
    iteration = int(input('Maximum Iteration: '))
    state = parseState(dataSplitted, pawnAmountBW) # generate an initial state
    result = simulatedAnnealing(state, pawnAmountBW, temperature, decreaseRate, iteration)
  elif (chosenAlgo == 3):
    populationAmount= int(input('Number Of Population: '))
    limit = int(input('Maximum generation: '))
    listOfStates = createListOfStates(dataSplitted, pawnAmountBW, populationAmount)
    result = geneticAlgorithm(listOfStates, pawnAmountBW, populationAmount, limit)

  # Print the result
  attackNum = countAtack(result) # Get the number of attack from the result state
  printBoard(result)
  print(attackNum['friend'], end='')
  print(' ', end='')
  print(attackNum['enemy'])

if __name__ == '__main__':
  main()