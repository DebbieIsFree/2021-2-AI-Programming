from problem import *
from optimizer import *

def selectProblem():
  print("Select the problem type: ")
  print("   1. Numerical Optimization")
  print("   2. TSP")   
  pType = int(input("Enter the number: ")) 
  if pType == 1:
    p = Numeric()  
  elif pType == 2:
    p = Tsp()
  return p, pType  # return problem & problem Type 


def selectAlgorithm(pType):
  print()
  print("Select the search algorithm:")
  print("   1. Steepest-Ascent")
  print("   2. First-Choice")      
  print("   3. Gradient Descent") 
  aType = int(input("Enter the number: "))
  invalid(pType, aType)  # Tsp문제는 gradient descent 사용 불가
  # 사용할 알고리즘 딕셔너리로 만들기 
  optimizer = { 1: 'SteepestAscent()', 
                2 : 'FirstChoice()', 
                3 : 'gradientDescent()'}
  alg = eval(optimizer[aType])    # 클래스 사용 
  alg.setVariables(aType, pType)  
  return alg
 

# Tsp 문제는 gradientDescent 알고리즘으로 풀 수 없음
def invalid(pType, aType):
  if(pType == 2 and aType == 3):
    print("\nYou cannot choose Gradient Descent with TSP")
    exit()  # 프로그램 종료


def main(): 
  p, pType = selectProblem()   # p : Numeric 또는 Tsp 객체 
  p.setVariables()  # 문제 유형에 따라 필드 초기화
  alg = selectAlgorithm(pType)  # 알고리즘 선택(객체 생성) 
  # Call the search algorithm
  alg.run(p)  
  # Show the problem and algorithm settings
  p.describe()
  alg.displaySetting()
  # Report results
  p.report()


main()
