from tsp import *

def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    

def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def mutants(current, p): # Apply inversion          
    n = p[0]          # 도시 개수
    neighbors = []    
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])  
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors


def bestOf(neighbors, p): # neighbors에 있는 mutants들의 값을 구해 가장 최적(최저)의 것을 리턴
    tmp = evaluate(neighbors[0], p)
    idx = 0

    for i in range(1, len(neighbors)):    
        if tmp > evaluate(neighbors[i], p):  
            tmp = evaluate(neighbors[i], p)
            idx = i
    bestValue = tmp
    best = neighbors[i]      
    return best, bestValue 


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")



main()
