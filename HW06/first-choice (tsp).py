from problem import Problem, Tsp

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    p = Tsp()  # Tsp 클래스의 객체 생성, 생성자 호출
    p.setVariables() # numCities, locations, table 구하기
    # Call the search algorithm
    firstChoice(p) 
    # Show the problem and algorithm settings
    p.describe()
    displaySetting() 
    # Report results
    p.displayResult(p.getSolution(), p.getValue())
    p.report()

def firstChoice(p): 
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current) # 'current'의 비용을 구함
    i = 0
    while i < LIMIT_STUCK:   # current보다 작은 successor가 없을 때 연속적으로 최대 100번까지만 실행 
        successor = p.randomMutant(current)    # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
        valueS = p.evaluate(successor)         # 위에서 구한 successor의 값을 구함
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC) # 객체의 메소드로 최적값 저장

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")


main()
