from problem import Problem, Numeric

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    p = Numeric()   # Numeric 클래스의 객체 생성, 생성자 호출
    p.setVariables()   # expression, domain 구하기
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.displayResult(p.getSolution(), p.getValue())
    p.report()

def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)   # 'current'의 값 구하기
    i = 0
    while i < LIMIT_STUCK:     # current 보다 작은 successor가 없을 때 최대 100번까지만 실행
        successor = p.randomMutant(current)    # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
        valueS = p.evaluate(successor)         # 'successor'의 값 구하기
        if valueS < valueC:                    # 최소화를 위해 current보다 successor의 값이 작으면 이동한 뒤 계속 반복
            current = successor                 
            valueC = valueS
            i = 0            # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC)  # p 객체의 메소드를 사용해 결과값 저장

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())


main()



