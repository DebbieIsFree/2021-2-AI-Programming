from tsp import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, distanceTable)
    # Call the search algorithm
    solution, minimum = firstChoice(p) 
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting() 
    # Report results
    displayResult(solution, minimum)


def firstChoice(p):   # 'p': (numCities, locations, distanceTable)
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p) # 'current'의 값을 구함
    i = 0
    while i < LIMIT_STUCK:   # current보다 작은 successor가 없을 때 최대 100번까지만 실행 
        successor = randomMutant(current, p)    # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
        valueS = evaluate(successor, p)         # 위에서 구한 successor의 값을 구함
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


def randomMutant(current, p): # Apply inversion
    while True:
        i, j = sorted([random.randrange(p[0])       # inversion할 거 랜덤으로 선택
                       for _ in range(2)])
        if i < j:
            curCopy = inversion(current, i, j)
            break
    return curCopy


def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")



main()
