from numeric import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)   # 'current'의 값 구하기
    i = 0
    while i < LIMIT_STUCK:      
        successor = randomMutant(current, p)    # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
        valueS = evaluate(successor, p)         # 'successor'의 값 구하기
        if valueS < valueC:                     # 최소화를 위해 current보다 successor의 값이 작으면 이동한 뒤 계속 반복
            current = successor                 
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


def randomMutant(current, p): ### 
    # successor을 구하기 위해 mutate 함수 사용, (current, i, d, p)에서 i와 d 값을 랜덤하게 선정
    size = len(p[1][0])     # 변수 개수
    opt = [-1 * DELTA, DELTA] 
    i = random.randint(0, size-1)  # i 번째 변수 랜덤 선택
    d = random.choice(opt)         # 델타값 랜덤 선택
    return mutate(current, i, d, p)  # Return a random successor



def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)



main()