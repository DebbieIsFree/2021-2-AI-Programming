import random
import math

class Problem():  # Numeric과 Tsp의 공통 부분을 Problem 클래스로 만들어 이를 상속함
  def __init__(self) -> None:   # return type : None
    self._solution = []
    self._value = 0
    self._numEval = 0

  # accessor
  def getNumEval(self):
    return self._numEval
  def getSolution(self):
    return self._solution
  def getValue(self):
    return self._value
  #mutator
  def setNumEval(self, cnt=0):
    self._numEval += cnt
  def storeResult(self, solution, value):
    self._solution = solution
    self._value = value
  def report(self):
    print()
    print("Total number of evaluations: {0:,}".format(self._numEval)) 



## Numeric Class
class Numeric(Problem):
  def __init__(self) -> None:
    super().__init__()
    self._delta = 0.01 
    self._domain = []     # domain = [varNames, low, up]
    self._expression = ''

    # Gradient Descent
    self._dx = 0.0001   # ε = pow(10, -4)
    self._alpha = 0.01  # update rate

  def getExpression(self):
    return self._expression

  def getDelta(self):
    return self._delta

  def setDelta(self, delta):
    self._delta = delta

  # Gradient Descent
  def getDx(self):
    return self._dx

  def getAlpha(self):
    return self._alpha

  def takeStep(self, current): 
    # gradient() 함수로 미분값 구하기
    # nextP가 domain에 주어진 범위를 넘지 않도록 isLegal()로 확인
    # nextP가 범위 안에 존재하면 nextP 반환, 그렇지 않으면 current 반환 
    nextp = self.gradient(current)    # nextP = f'(x) * alpha
    for i in range(len(nextp)):
      nextp[i] = current[i] - nextp[i]   # nextP = currentP - (alpha * f'(x))
    if(self.isLegal(nextp)):
      return nextp
    else:
      return current

  def gradient(self, current):   # 미분값 f'(x)에 alpha 곱한 값 구하기 
    varNames = self._domain[0]   # 변수 개수 
    nextp = []
    f = self.evaluate(current)   # 현재 지점(current)에 대한 함숫값 구하기
    # i-th partial derivative 구하기 : f(x_ith') - f(x) / δ
    # x_ith' : i번째 변수에 ε = pow(10, -4) 값 더하기 
    for i in range(len(varNames)):
      copy = current[:]
      copy[i] = copy[i] + self._dx  # dx = 0.0001
      derived_f = self.evaluate(copy)
      tmp = (derived_f - f) / self._dx * self._alpha
      nextp.append(tmp)
    return nextp

  def isLegal(self, nextP):    # f'(x) * alpha 범위 검사
    for i in range(len(nextP)):
      l = self._domain[1][i]
      u = self._domain[2][i]
      if l > nextP[i] or  u < nextP[i]:
        return False
    return True

  def setVariables(self):
      ## Read in an expression and its domain from a file.  
      ## 'expression' is a string.
      ## 'domain' is a list of 'varNames', 'low', and 'up'.
      ## 'varNames' is a list of variable names.
      ## 'low' is a list of lower bounds of the varaibles.
      ## 'up' is a list of upper bounds of the varaibles.
      fileName = input("Enter the file name of a function: ")
      infile = open(fileName, 'r')
      self._expression = infile.readline()   # 수식 구하기
      varNames =[]                    
      low = []
      up = []
      line = infile.readline()
      while(line != ""):   # 파일을 한 줄씩 읽어들이며 domain 구하기 
          data = line.split(',')
          varNames.append(data[0])
          low.append(float(data[1]))
          up.append(float(data[2]))
          line = infile.readline()
      infile.close()
      self._domain = [varNames, low, up]
      
  def randomInit(self): # Return a random initial point as a list of values
      init = [] 
      for i in range(len(self._domain[0])):   # 변수 개수 만큼 반복
          l = self._domain[1][i]              # i번째 변수의 lower bound
          u = self._domain[2][i]              # i번째 변수의 upper bound
          tmp = random.uniform(l, u) 
          init.append(tmp)
      return init    

  def evaluate(self, current):  
      ## Evaluate the expression after assigning
      ## the values of 'current' to the variables
      self.setNumEval(1)
      expr = self._expression       # function expression
      varNames = self._domain[0]    # domain: [varNames, low, up]
      for i in range(len(varNames)):
          assignment = varNames[i] + '=' + str(current[i])  
          exec(assignment)    # 각 변수에 값 대입
      return eval(expr)       # 수식 계산한 값 리턴

  def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
      curCopy = current[:]
      domain = self._domain   # [VarNames, low, up]
      l = domain[1][i]     # Lower bound of i-th
      u = domain[2][i]     # Upper bound of i-th
      if l <= (curCopy[i] + d) <= u: 
          curCopy[i] += d  
      return curCopy  # i 번째 변수에 d만큼 더한 값이 범위 안에 있으면 리턴

  # FCHC-N
  def randomMutant(self, current): 
      # successor를 구하기 위해 mutate 함수 사용
      # (current, i, d, p)에서 i와 d 값을 랜덤하게 선정
      size = len(self._domain[0])     # 변수 개수
      opt = [-1 * self._delta, self._delta] 
      i = random.randint(0, size-1)  # i 번째 변수 랜덤 선택
      d = random.choice(opt)         # 델타값 랜덤 선택
      return self.mutate(current, i, d)  # Return a random successor

  # SAHC-N
  def mutants(self, current): 
      neighbors = []
      opt = [self._delta, -1*self._delta]
      # i번째 변수를 delta, -delta만큼 바꾼 값을 successor로 하여 
      # neighbors에 추가 (current에서 가능한 모든 경우 탐색)
      for i in range(len(self._domain[0])):  
          for delta in opt:
              m = self.mutate(current, i, delta)
              neighbors.append(m)
      return neighbors     # Return a set of successors   

  def describe(self):
      print()
      print("Objective function:")
      print(self._expression)     # Expression
      print("Search space:")
      varNames = self._domain[0]  # domain: [VarNames, low, up]
      low = self._domain[1]
      up = self._domain[2]
      for i in range(len(low)):
          print(" " + varNames[i] + ":", (low[i], up[i])) 

  def displayResult(self, solution, minimum):
      print()
      print("Solution found:")
      print(self.coordinate(solution))  # Convert list to tuple
      print("Minimum value: {0:,.3f}".format(minimum))

  def coordinate(self, solution):
      c = [round(value, 3) for value in solution]
      return tuple(c)  # Convert the list to a tuple



## TSP Class
class Tsp(Problem):
  def __init__(self) -> None:
    super().__init__()
    self._numCities = 0
    self._locations = []
    self._table = [ [0] * self._numCities for _ in range(self._numCities) ]

  def setVariables(self):
    ## Read in a TSP (# of cities, locatioins) from a file.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    self._numCities = int(infile.readline())
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        self._locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    self.calcDistanceTable(self._numCities, self._locations)  
  
  def calcDistanceTable(self, numCities, locations): ### 두 지점간 거리 table 만들기   
      table = [ [0] * numCities for _ in range(numCities) ]
      for i in range(numCities):
          for j in range(numCities):
              From  = list(locations[i])
              To = list(locations[j])
              distance =  math.sqrt((From[0]-To[0])**2 + (From[1] - To[1])**2)
              table[i][j] = round(distance, 1)
      self._table = table
            
  def randomInit(self):   # Return a random initial tour
      n = self._numCities         # 도시 개수 
      init = list(range(n))       # 도시 개수만큼 번호 만들기
      random.shuffle(init)        # 방문할 도시 순서 섞기
      return init

  def evaluate(self, current): ###   
      ## Calculate the tour cost of 'current'
      ## 'current' is a list of city ids
      self.setNumEval(1)
      cost = 0
      table = self._table
      From = current[0]
      To = current[0]
      # calcDistanceTable 메서드에서 구한 table을 이용해서 각 도시를 방문하는 비용의 총합(cost) 구하기
      for i in range(1, len(current)):
          From = To
          To = current[i]
          cost += table[From][To]
      return cost  

  def inversion(self, current, i, j):  ## Perform inversion
      curCopy = current[:]
      while i < j:
          curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
          i += 1
          j -= 1
      return curCopy

  # FCHC-TSP
  def randomMutant(self, current): # Apply inversion
      while True:
          i, j = sorted([random.randrange(self._numCities)     # inversion할 거 랜덤으로 선택
                        for _ in range(2)])
          if i < j:
              curCopy = self.inversion(current, i, j)
              break
      return curCopy

  # SAHC-TSP
  def mutants(self, current): # Apply inversion          
      n = self._numCities     # 도시 개수
      neighbors = []    
      count = 0
      triedPairs = []
      while count <= n:  # Pick two random loci for inversion
          i, j = sorted([random.randrange(n) for _ in range(2)])
          if i < j and [i, j] not in triedPairs:
              triedPairs.append([i, j])  
              curCopy = self.inversion(current, i, j)
              count += 1
              neighbors.append(curCopy)
      return neighbors  # 가능한 모든 경우를 다 탐색해 리턴

  def describe(self):
      print()
      n = self._numCities
      print("Number of cities:", n)
      print("City locations:")
      locations = self._locations
      for i in range(n):
          print("{0:>12}".format(str(locations[i])), end = '')
          if i % 5 == 4:
              print()

  def displayResult(self, solution, minimum):
      print()
      print("Best order of visits:")
      self.tenPerRow(solution)       # Print 10 cities per row
      print("Minimum tour cost: {0:,}".format(round(minimum)))
      
  def tenPerRow(self, solution):
      for i in range(len(solution)):
          print("{0:>5}".format(solution[i]), end='')
          if i % 10 == 9:
              print()