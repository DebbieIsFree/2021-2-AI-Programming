import random
import math

NumEval = 0    # Total number of evaluations

def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []

    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)  
    return numCities, locations, table


def calcDistanceTable(numCities, locations): ### 두 지점간 거리 table 만들기   
    table = [ [0] * numCities for _ in range(numCities) ]

    for i in range(numCities):
        for j in range(numCities):
            From  = list(locations[i])
            To = list(locations[j])
            distance =  math.sqrt((From[0]-To[0])**2 + (From[1] - To[1])**2)
            table[i][j] = round(distance, 1)
    return table # A symmetric matrix of pairwise distances 


def randomInit(p):   # Return a random initial tour
    n = p[0]                    # 도시 개수 
    init = list(range(n))       # 도시 개수만큼 번호 만들기
    random.shuffle(init)        # 방문할 도시 순서 섞기
    return init


def evaluate(current, p): ###   
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
   
    global NumEval
    NumEval += 1
    cost = 0
    table = p[2]
    From = current[0]
    To = current[0]
    
    # createProblem 함수에서 구한 table을 이용해서 각 도시를 방문하는 비용의 총합(cost) 구하기
    for i in range(1, len(current)):
        From = To
        To = current[i]
        cost += table[From][To]
    return cost  


def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy


def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()


def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))


def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()

