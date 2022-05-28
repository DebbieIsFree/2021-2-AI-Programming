from problem import Problem, Numeric

def main():
    # Create an instance of numerical optimization problem  
    p = Numeric() # Numeric 객체 생성, 생성자 호출
    p.setVariables() # domain, expression 구함
    # Call the search algorithm
    gradientDescent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.displayResult(p.getSolution(), p.getValue())
    p.report()

def gradientDescent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current) # 'current' 값 계산
    while True:      
        nextP = p.takeStep(current) # current에서 이동할 next point 구하기
        valueN = p.evaluate(nextP)  # next point에서 값 계산
        if valueN < valueC:                     
            current = nextP               
            valueC = valueN
        else:
            break
    p.storeResult(current, valueC)   

def displaySetting(p):  
    print()
    print("Search algorithm: Gradient Descent")
    print()
    print("Alpha rate:", p.getAlpha())

main()
