from problem import Problem, Tsp

def main():
    p = Tsp()  # Tsp 클래스 객체 생성, 생성자 호출
    p.setVariables() # numCities, location, table 구함
    # Call the search algorithm
    steepestAscent(p)
    #  Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.displayResult(p.getSolution(), p.getValue())
    p.report()
    
def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current) # current 순서의 비용 구함
    while True:
        neighbors = p.mutants(current) # 가능한 모든 경우 다 탐색
        (successor, valueS) = bestOf(neighbors, p) # 그 중 최적의 값 선택
        if valueS >= valueC: 
            break
        else:
            current = successor  # current보다 작은 값이 있으면 계속 갱신
            valueC = valueS
    p.storeResult(current, valueC) # 객체의 메소드로 결과값 저장


def bestOf(neighbors, p): # neighbors에 있는 mutants들의 값을 구해 가장 최적(최저)의 것을 리턴
    tmp = p.evaluate(neighbors[0])
    idx = 0

    for i in range(1, len(neighbors)):    
        if tmp > p.evaluate(neighbors[i]):  
            tmp = p.evaluate(neighbors[i])
            idx = i
    bestValue = tmp
    best = neighbors[idx]      
    return best, bestValue 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")



main()
