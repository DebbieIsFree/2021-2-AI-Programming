import random
import math
from setup import Setup


class Problem(Setup):  # Numeric과 Tsp의 공통 부분을 Problem 클래스로 만들어 상속함
  def __init__(self): 
    Setup.__init__(self)  
    self._pFileName = ''      
    self._solution = []       # best solution
    self._value = 0           # best minimum
    self._numEval = 0         # sum of numEval
    self._avgMinimum = 0
    self._avgNumEval = 0
    self._avgWhen = 0           

  def getNumEval(self):
    return self._numEval

  def getSolution(self):
    return self._solution

  def getValue(self):
    return self._value

  def setVariables(self, parameters):        
    self._pFileName = parameters['pFileName']
    Setup.setVariables(self, parameters)

  def storeResult(self, solution, value):  
    self._solution = solution
    self._value = value

  def reportNumEvals(self):        
    if 1 <= self._aType <= 4:
      print("Total number of evaluations: {0:,}".format(self._numEval)) 

  def report(self):    
    if 5 <= self._aType == 6:
      print("\naverage iteration of finding the best: {0:,}".format(self._avgWhen))
    print()
         
  def randomInit(self):
    pass
  
  def evaluate(self):
    pass

  def mutants(self):
    pass

  def randomMutant(self, current):
    pass

  def describe(self):
    pass

  def storeExpResult(self, results):
    self._solution, self._value, self._avgMinimum, self._avgNumEval, self._numEval,  self._avgWhen = results
    
  def initializePop(self, size):       
    pass

  def evalInd(self, ind):        
    pass

  def crossover(self, ind1, ind2, pC):
    pass

  def uXover(self, chrInd1, chrInd2, pC):
    pass

  def mutation(self, ind, pM): 
    pass

  def indToSol(self, ind): 
    pass
  # print할 때, solution을 찾은 index가 어디인지 출력하는 것 (bestSolution 출력하는 것)  





class Numeric(Problem):
  def __init__(self) :
    super().__init__()
    self._domain = []     # domain = [varNames, low, up]
    self._expression = ''

  def getExpression(self):
    return self._expression

  def takeStep(self, current):  
    nextp = self.gradient(current)      # nextP =  alpha * f'(x)
    for i in range(len(nextp)):
      nextp[i] = current[i] - nextp[i]  # nextP = currentP - (alpha * f'(x))
    if(self.isLegal(nextp)):
      return nextp
    else:
      return current

  def gradient(self, current):   # 미분값 f'(x)에 alpha 곱한 값 구하기 
    varNames = self._domain[0]   # 변수 개수 
    nextp = []
    f = self.evaluate(current)   # 현재 지점(current)에 대한 함숫값 구하기
    # i-th partial derivative 구하기 
    # x_ith' : i번째 변수에 ε = pow(10, -4) 값 더하기 
    for i in range(len(varNames)):
      copy = current[:]
      copy[i] = copy[i] + self._dx  
      derived_f = self.evaluate(copy)
      tmp = (derived_f - f) / self._dx * self._alpha
      nextp.append(tmp)
    return nextp

  def isLegal(self, nextP):    # f'(x) * alpha 범위 검사
    for i in range(len(nextP)):
      l = self._domain[1][i]
      u = self._domain[2][i]
      if l > nextP[i] or  u < nextP[i]: # 범위를 벗어나면 false 반환
        return False 
    return True

  def setVariables(self, parameters):
    Problem.setVariables(self, parameters)        
    infile = open(self._pFileName, 'r')
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
    self._numEval += 1
    expr = self._expression       
    varNames = self._domain[0]   
    for i in range(len(varNames)):
      assignment = varNames[i] + '=' + str(current[i])  
      exec(assignment)      # 각 변수에 값 대입
    return eval(expr)       # 수식 계산한 값 리턴

  def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = self._domain   
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u: 
      curCopy[i] += d  
    return curCopy  # i 번째 변수에 d만큼 더한 값이 범위 안에 있으면 리턴

  # FCHC-N
  def randomMutant(self, current): 
    # successor를 구하기 위해 mutate 함수 사용
    # (current, i, d, p)에서 i와 d 값을 랜덤하게 선정
    size = len(self._domain[0])    
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
    print(self._expression)     
    print("Search space:")
    varNames = self._domain[0]  
    low = self._domain[1]
    up = self._domain[2]
    for i in range(len(low)):
      print(" " + varNames[i] + ":", (low[i], up[i])) 

  def report(self):
    print()
    print("Average objective value: {0:,.3f}" .format(self._avgMinimum))                
    print("Average number of evaluations: {0:,}" .format(self._avgNumEval))
    print()
    print("Best solution found:")
    print(self.coordinate(self._solution))  # Convert the list to a tuple
    print("Best value: {0:,.3f}".format(self._value))
    super().report()
    self.reportNumEvals()         ##################

  def coordinate(self, solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple


  def initializePop(self, size):  # design chromosome set   
    pop = []
    for i in range(size):  # popSize만큼 chromosome 만들기
      chromosome = self.randBinStr()  
      pop.append([0, chromosome])   # 앞에 0은 fitness 값
    return pop


  def randBinStr(self):       # create binary string randomly
    k = len(self._domain[0]) * self._resolution  # domain[0] : 변수 개수
    chromosome = []    
    for i in range(k):              
      allele = random.randint(0,1)  # allele : 대립 유전자  0 or 1 중 랜덤 선택
      chromosome.append(allele)
    return chromosome   # len(domain[0]) * resolution 길이의 string 랜덤 생성


  def evalInd(self, ind):  # ind : [fitness, chromosome]
    ind[0] = self.evaluate(self.decode(ind[1]))  # Record fitness    


  # randBinStr()으로 만든 binary 형태의 chromosome을
  # (resolution)자리의 10진수로 decode 한다. 
  def decode(self, chromosome):
    r = self._resolution
    low = self._domain[1]  # list of lower bounds
    up = self._domain[2]   # list of upper bounds
    genotype = chromosome[:]   # binary 형태
    phenotype = []   # output
    start = 0
    end = r 
    for var in range(len(self._domain[0])):   # 변수 개수만큼 반복
      value = self.binaryToDecimal(genotype[start:end], low[var], up[var])
      phenotype.append(value)   
      start += r    # resolution마다 반복
      end += r
    return phenotype  


  def binaryToDecimal(self, binCode, l, u):   # binCode == genotype
    r = len(binCode)   # resolution = binary 코드의 길이
    decimalValue = 0
    for i in range(r):
      decimalValue += binCode[i] * (2 ** (r-1-i))   # 10진수로 바꿔주는 코드 
    return l + (u-l) * decimalValue / 2**r   # lower, upper bound 안의 값으로 바꾸기 위한 연산 추가


  def crossover(self, ind1, ind2, pC): 
    # pC is interpreted as uXp  # (probability of swap)
    chr1, chr2 = self.uXover(ind1[1], ind2[1], pC) 
    return [0, chr1], [0, chr2]   # 앞에 fitness 값 0으로 초기 설정
  

  def uXover(self, chrInd1, chrInd2, pC):  
    chr1 = chrInd1[:]    # Make copies
    chr2 = chrInd2[:] 
    for i in range(len(chr1)):
      if random.uniform(0, 1) < pC:   # 0~1 사이 난수 생성
        chr1[i], chr2[i] = chr2[i], chr1[i]  # 값 서로 바꾸기
    return chr1, chr2


  def mutation(self, ind, pM):   # ind : [fitness, chromosome]
    opt = [i for i in range(0, len(ind[1]))]  # mutation되는 인덱스 랜덤 선택
    ith = random.choice(opt)
    if random.uniform(0, 1) <  1 / pM:
      if ind[1][ith] == 1:
        ind[1][ith] = 0
      else:
        ind[1][ith] = 1
    

  def indToSol(self, ind):
    solution = self.decode(ind[1])
    value = self.evaluate(solution)
    self.storeResult(solution, value)




class Tsp(Problem):
  def __init__(self) :
    Problem.__init__(self)
    self._numCities = 0
    self._locations = []
    self._table = [ [0] * self._numCities for _ in range(self._numCities) ]

  def setVariables(self, parameters):
    # Read in a TSP (# of cities, locatioins) from a file.
    # First line is number of cities
    Problem.setVariables(self, parameters)
    infile = open(self._pFileName, 'r')
    self._numCities = int(infile.readline())
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
      self._locations.append(eval(line)) # Make a tuple and append
      line = infile.readline()
    infile.close()
    self.calcDistanceTable(self._numCities, self._locations)  
  
  def calcDistanceTable(self, numCities, locations): # 두 지점간 거리 table 만들기   
    table = [ [0] * numCities for _ in range(numCities) ]
    for i in range(numCities):
      for j in range(numCities):
        From  = list(locations[i])
        To = list(locations[j])
        distance =  math.sqrt((From[0]-To[0])**2 + (From[1] - To[1])**2)  
        table[i][j] = round(distance, 1)
    self._table = table
            
  def randomInit(self):   # Return a random initial tour
    n = self._numCities         
    init = list(range(n))       # 도시 개수만큼 번호 만들기
    random.shuffle(init)        # 방문할 도시 순서 섞기
    return init

  def evaluate(self, current):  
    ## Calculate the tour cost of 'current'
    ## 'current' is a list of city ids
    self._numEval += 1
    cost = 0
    table = self._table
    From = current[0]
    To = current[0]
    # table을 이용해서 각 도시를 방문하는 비용 총합(cost) 구하기
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
      i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
      if i < j:
        curCopy = self.inversion(current, i, j)
        break
    return curCopy

# SAHC-TSP
  def mutants(self, current): # Apply inversion          
    n = self._numCities     
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

  def report(self):
    print()
    print("Average cost: {0:,.3f}" .format(self._avgMinimum))         
    print("Average number of evaluations: {0:,}" .format(self._avgNumEval))
    print()
    print("Best order of visits:")
    self.tenPerRow(self._solution)   # Print 10 cities per row
    print("Best tour cost: {0:,}".format(round(self._value)))
    super().report()
    self.reportNumEvals()         ######
      
  def tenPerRow(self, solution):
    for i in range(len(solution)):
      print("{0:>5}".format(solution[i]), end='')
      if i % 10 == 9:
        print()
        
  def initializePop(self, size):
    pop = []
    for i in range(size):  # popSize만큼 individual만들기
      chromosome = self.randomInit()  
      pop.append([0, chromosome])   # 앞에 0은 fitness (=evaluation) 값
    return pop


  def evalInd(self, ind):  # 미리 만들어둔 distance table을 이용해 fitness 값 구하기
    ind[0] = self.evaluate(ind[1])   # Record fitness  
      

  def crossover(self, ind1, ind2, pC):
    if random.uniform(0, 1) < pC : 
      chr1, chr2 = self.oXover(ind1[1], ind2[1]) 
      return [0, chr1], [0, chr2]
    else:
      return ind1, ind2


  def oXover(self, chrind1, chrind2): 
    point = random.sample(range(0,len(chrind1)),2)   # 0부터 len(chrind1)-1까지의 범위중에 2개를 중복없이 선택    
    point.sort()      # CrossOver line 랜덤 선택 후 정렬 
    p1 = point[0]     # random CrossOver line 1
    p2 = point[1]     # random CrossOver line 2

    ch1 = chrind1[p1:p2+1]      # 자손1은 부모1의 p1~p2 사이의 값을 가짐
    ch2 = chrind2[p1:p2+1]      # 자손2는 부모 2의 p1~p2 사이의 값을 가짐

    tmp1 = []
    for i in chrind2:      # 자손1의 나머지(자손1에 없는 값)는 부모2에서 가져옴 (tmp1에 저장)
      if i not in ch1:    
        tmp1.append(i)
    
    cnt = 0
    for i in range(len(chrind1)-p2):    # 자손1) ch1[p2+1:]을 구현   
      if len(tmp1) != 0:
        ch1.append(tmp1[0])  
        del(tmp1[0])
        cnt += 1
    ch1 = tmp1 + ch1    # 자손1) ch1[:p1]을 구현

    tmp2 = []
    for i in chrind1:     # 자손2의 나머지(자손2에 없는 값)는 부모1에서 가져옴 (tmp2에 저장)
      if i not in ch2:
        tmp2.append(i)
  
    cnt2 = 0
    for i in range(len(chrind2)-p2):    # 자손2) ch2[p2+1:]을 구현
      if len(tmp2) != 0:
        ch2.append(tmp2[0])
        del(tmp2[0])
        cnt2 += 1
    ch2 = tmp2 + ch2    # 자손2) ch2[:p1]을 구현
    return ch1, ch2  # crossover된 두 개의 자손 리턴 



  def mutation(self, ind, pM):
    # swap할 두 도시를 랜덤 선택 
    a, b = random.sample(range(0,len(ind[1])),2)
    if random.random() < pM:
      ind[1][a], ind[1][b] = ind[1][b], ind[1][a]


  def indToSol(self, ind):
    solution = ind[1]
    value = ind[0]
    self.storeResult(solution, value)