from numeric import *


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain),   'domain' : [varNames, low, up]
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p) # 'current' 비용 계산
    while True:
        neighbors = mutants(current, p)  # 'current' 기준으로 가능한 모든 successor를 구해서 neighbors에 추가
        successor, valueS = bestOf(neighbors, p)  # neighbors에서 최적의 것을 successor로 선택
        if valueS >= valueC:                      # successor와 current를 비교해서 작은 값을 취함(이동)
            break
        else:
            current = successor 
            valueC = valueS
    return current, valueC    


def mutants(current, p): 
    neighbors = []
    opt = [DELTA, -1*DELTA]
    
    for i in range(len(p[1][0])):  # i번째 변수를 DELTA, -DELTA만큼 바꾼 값을 successor로 하여 neighbors에 추가
        for delta in opt:
            m = mutate(current, i, delta, p)
            neighbors.append(m)
    return neighbors     # Return a set of successors   


def bestOf(neighbors, p):  # neighbors에 있는 mutants들의 값을 구해 가장 최적(최저)의 값을 리턴
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
    print()
    print("Mutation step size:", DELTA)



main()
