from problem import Problem, Numeric

def main():
    p = Numeric()   # Numeric 클래스 객체 생성, 생성자 호출
    p.setVariables()  # expression, domain 구하기
    # Call the search algorithm
    steepestAscent(p)  

    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p) 
    #  Report results
    p.displayResult(p.getSolution(), p.getValue())
    p.report()

def steepestAscent(p):
    # p 객체의 메소드를 사용해서 
    # 리스트 형태의 current (initial point) 랜덤하게 구하기 & 값 계산
    current = p.randomInit() 
    valueC = p.evaluate(current)  # 현재 지점 값 계산
    while True:
        neighbors = p.mutants(current)  # 'current' 기준으로 가능한 모든 successor를 구해서 neighbors에 추가
        successor, valueS = bestOf(neighbors, p)    # neighbors에서 최적의 것을 successor로 선택
        if valueS >= valueC:     # successor와 current를 비교해서 작은 값을 취함(이동)
            break
        else:      
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)
   

# neighbors에 있는 mutants들의 값을 구해 가장 최적(최저)의 값을 리턴
def bestOf(neighbors, p):  
    tmp = p.evaluate(neighbors[0]) 
    idx = 0

    for i in range(1, len(neighbors)):   
        if tmp > p.evaluate(neighbors[i]):
            tmp = p.evaluate(neighbors[i])
            idx = i
    bestValue = tmp
    best = neighbors[idx]        
    return best, bestValue


def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())



main()
