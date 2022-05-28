from problem import Problem
from setup import Setup
import random, math


class Optimizer(Setup):
  def __init__(self):
    Setup.__init__(self)
    self._pType = 0
    self._numExp = 0

  def setVariables(self, parameters):
    Setup.setVariables(self, parameters)
    self._pType = parameters['pType']
    self._numExp = parameters['numExp']


  def getAType(self):
    return self._aType      

  def getNumExp(self):
    return self._numExp

  def displayNumExp(self):     # Total number of experiments
    print()
    print("Number of experiments: ", self._numExp)

  def displaySetting(self):        
    if self._pType == 1 and self._aType != 4 and self._aType != 6:
      print("Mutation step size:", self._delta)       
  


class HillClimbing(Optimizer):   
  def __init__(self):       
    Optimizer.__init__(self)  
    self._limitStuck = 100      
    self._numRestart = 0        

  def setVariables(self, parameters):
    super().setVariables(parameters)
    self._limitStuck = parameters['limitStuck']
    self._numRestart = parameters['numRestart']

  def randomRestart(self, p):   
    solutions = []
    values= []
    for i in range(self._numRestart):
      self.run(p)
      solutions.append(p.getSolution())
      values.append(p.getValue())
    minValue = min(values)
    idx = values.index(minValue)
    p.storeResult(solutions[idx], minValue)
  

  def run(self, p): 
    pass

  def displaySetting(self):  # Hill Climbing 알고리즘에서 공통적으로 사용되는 정보
    print("\nNumber of random restarts: ", self._numRestart)
    print()
    super().displaySetting()       
    if(self._aType == 2 or self._aType == 3):
      print("Max evaluations with no improvement:", self._limitStuck, "iterations")          



class SteepestAscent(HillClimbing):
  def displaySetting(self):  
    print("\nSearch Algorithm: SteepestAscent HillClimbing")  
    HillClimbing.displaySetting(self)  
     
  def run(self, p): 
    current = p.randomInit() 
    valueC = p.evaluate(current) 
    while True:
      neighbors = p.mutants(current)  # 'current' 기준으로 가능한 모든 successor를 구해서 neighbors에 추가
      successor, valueS = self.bestOf(neighbors, p)   # neighbors에서 최적의 것을 successor로 선택
      if valueS >= valueC:    # successor와 current를 비교해서 작은 값을 취함(이동)
        break
      else:      
        current = successor
        valueC = valueS
    p.storeResult(current, valueC)  

  def bestOf(self, neighbors, p):  # neighbors에서 최적의 값 구하기
    tmp = p.evaluate(neighbors[0]) 
    idx = 0
    for i in range(1, len(neighbors)):   
      if tmp > p.evaluate(neighbors[i]):
        tmp = p.evaluate(neighbors[i])
        idx = i
    bestValue = tmp
    best = neighbors[idx]        
    return best, bestValue  
 


class FirstChoice(HillClimbing):  
  def displaySetting(self):   
    print("\nSearch Algorithm: First Choice Hill Climbing")  
    HillClimbing.displaySetting(self)             
 
  def run(self, p):  
    current = p.randomInit()       # 초기값 랜덤으로 구하기
    valueC = p.evaluate(current) 
    i = 0      
    while i < self._limitStuck:     # current 보다 작은 successor가 없을 때 최대 100번까지만 실행
      successor = p.randomMutant(current)  # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
      valueS = p.evaluate(successor)       # 'successor'의 값 구하기
      if valueS < valueC:         # 최소화를 위해 current보다 successor의 값이 작으면 이동한 뒤 계속 반복
        current = successor                 
        valueC = valueS
        i = 0        # Reset stuck counter
      else:
        i += 1
    p.storeResult(current, valueC) 



class gradientDescent(HillClimbing):   
  def displaySetting(self): 
    print("\nSearch Algorithm: Gradient Descent HillClimbing")  
    print("Update rate for gradient descent: ", self._alpha)   
    print("Increment for calculating derivatives: ", self._dx)         
    HillClimbing.displaySetting(self)             

  def run(self, p):  
    current = p.randomInit()     # 초기값 랜덤 설정
    valueC = p.evaluate(current) # current 값 계산
    while True:      
      nextP = p.takeStep(current) # current에서 이동할 next point 구하기
      valueN = p.evaluate(nextP)  # next point에서 값 계산
      if valueN < valueC:                     
        current = nextP               
        valueC = valueN
      else:
        break
    p.storeResult(current, valueC)  
 


class Stochastic(HillClimbing):
  def displaySetting(self):  
    print("\nSearch Algorithm: Stochastic HillClimbing")  
    HillClimbing.displaySetting(self)

  def run(self, p):
    current = p.randomInit() 
    valueC = p.evaluate(current)
    i = 0
    while i < self._limitStuck:     
      neighbors = p.mutants(current)  # Stochastic hill climbing generates multiple neighbors
      successor, valueS = self.stochasticBest(neighbors, p)   # selects one from them at random by a probability proportional to the quality.
      if valueS < valueC:        
        current = successor                 
        valueC = valueS
        i = 0        # Reset stuck counter
      else:
        i += 1
    p.storeResult(current, valueC)

  def stochasticBest(self, neighbors, p):
    # Smaller valuse are better in the following list
    valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
    largeValue = max(valuesForMin) + 1
    valuesForMax = [largeValue - val for val in valuesForMin]
    # Now, larger values are better
    total = sum(valuesForMax)
    randValue = random.uniform(0, total)
    s = valuesForMax[0]
    for i in range(len(valuesForMax)):
      if randValue <= s: # The one with index i is chosen
        break
      else:
        s += valuesForMax[i+1]
    return neighbors[i], valuesForMin[i]



class MetaHeuristics(Optimizer):
  def __init__(self):
    Optimizer.__init__(self)       
    self._limitEval = 0
    self._whenBestFound = 0

  def setVariables(self, parameters):
    Optimizer.setVariables(self, parameters)
    self._limitEval = parameters['limitEval']

  def getWhenBestFound(self):         
    return self._whenBestFound

  def displaySetting(self):
    Optimizer.displaySetting(self)
    print("Number of evaluations until termination: {0:,}".format(self._limitEval))




class SimulatedAnnealing(MetaHeuristics):
  def __init__(self):
    MetaHeuristics.__init__(self)
    self._numSample = 100    

  def displaySetting(self):
    print("\nSearch Algorithm: Simulated Annealing")
    print()
    MetaHeuristics.displaySetting(self)

  def run(self, p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    t = self.initTemp(p)        # 초기 temperature 구하기
    i = 0
    while True:
      t = self.tSchedule(t)   # next temperature 구하기
      if t == 0 or i == self._limitEval:   # 종료 조건 
        break
      nextP = p.randomMutant(current)  # successor 구하기
      valueN = p.evaluate(nextP)  
      dE = valueN - valueC    
      if (dE < 0) :     # 현재보다 더 좋은 값이면 갱신                 
        current = nextP               
        valueC = valueN
        self._whenBestFound = i    # dE < 0 이면 best solution 발생 시점 갱신 
      elif random.uniform(0,1) <= math.exp(-dE/t) :  # 나쁜 해도 확률적으로 받아들임
        current = nextP               
        valueC = valueN  
      i += 1
    p.storeResult(current, valueC)


  # initTemp returns an initial temperature such that the probability of accepting a worse neighbor
  def initTemp(self, p): # To set initial acceptance probability to 0.5
    diffs = []
    for i in range(self._numSample):      
      c0 = p.randomInit()     # A random point
      v0 = p.evaluate(c0)     # Its value
      c1 = p.randomMutant(c0) # A mutant
      v1 = p.evaluate(c1)     # Its value
      diffs.append(abs(v1 - v0))
    dE = sum(diffs) / self._numSample  # Average value difference
    t = dE / math.log(2)        # exp(–dE/t) = 0.5
    return t

  # tSchedule returns the next temperature according to an annealing schedule.
  def tSchedule(self, t):
    return t * (1 - (1 / 10**4))




class GA(MetaHeuristics):
  def __init__(self):
    MetaHeuristics.__init__(self)
    self._popSize = 0     # Population size
    self._uXp = 0   # Probability of swappping a locus for Xover  
    self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation  
    self._XR = 0    # Crossover rate for permutation code  
    self._mR = 0    # Mutation rate for permutation code
    self._pC = 0    # Probability parameter for Xover
    self._pM = 0    # Probability parameter for mutation

  def setVariables(self, parameters):
    MetaHeuristics.setVariables(self, parameters)
    self._popSize = parameters['popSize']         
    self._uXp = parameters['uXp']
    self._mrF = parameters['mrF']
    self._XR = parameters['XR']
    self._mR = parameters['mR']
    if self._pType == 1:    # Numeric
      self._pC = self._uXp
      self._pM = self._mrF
    if self._pType == 2:    # Tsp
      self._pC = self._XR
      self._pM = self._mR

  def displaySetting(self):
    print()
    print("Search Algorithm: Genetic Algorithm")
    print()
    MetaHeuristics.displaySetting(self)
    print()
    print("Population size:", self._popSize)
    if self._pType == 1:   # Numeric
      print("Number of bits for binary encoding:", self._resolution)
      print("Swap probability for uniform crossover:", self._uXp)
      print("Multiplication factor to 1/L for bit-flip mutation:",self._mrF)
    elif self._pType == 2: # TSP
      print("Crossover rate:", self._XR)
      print("Mutation rate:", self._mR)

  def run(self, p):
    popSize = self._popSize
    pop = p.initializePop(popSize)       # population set 생성
    best = self.evalAndFindBest(pop, p)  # 0인 evaluation 값을 계산해서 바꾸고,
                                         # 값이 가장 작은 individual 찾기 
    for j in range(self._limitEval): 
      newPop = []
      i = 0                       
      while i < self._popSize:    # 모든 population에 대해 crossover & mutation 
        par1, par2 = self.selectParents(pop)
        ch1, ch2 = p.crossover(par1, par2, self._pC)  
        p.mutation(ch1, self._pM)   # crossover해서 만든 자손 2개를 각각 mutation 
        p.mutation(ch2, self._pM)   
        newPop.extend([ch1, ch2])
        i += 2             ## 2씩 증가 ch1, ch2
      next = self.evalAndFindBest(newPop, p)
      if next[0] < best[0] :       # 현재 population의 최적의 indvidual보다 successor의 것이 더 
        best = next                # 작은 값을 가지면 최적해 및 population 갱신
        pop = newPop
        self._whenBestFound = j    # 최적해를 찾은 순간 기록
      # else:             
      #   break
    p.indToSol(best)
    
  

  def evalAndFindBest(self, pop, p):  
    # Eval
    for i in range(self._popSize):
      p.evalInd(pop[i])
    # Find Best  
    best = pop[0][0]
    idx = 0
    for j in range (1, self._popSize):
      if pop[j][0] < best:  # fitness 값이 가장 작은 chromosome을 구함
        best = pop[j][0]
        idx = j
    return pop[idx]


  def selectParents(self, pop):
    ind1, ind2 = self.selectTwo(pop)           # 자손해를 만들 부모 2개 선택
    par1 = self.binaryTournament(ind1, ind2)   # fitness 값이 더 작은거 선택
    ind1, ind2 = self.selectTwo(pop)           # 한 번 더 반복
    par2 = self.binaryTournament(ind1, ind2)
    return par1, par2    # parent1, parent2 return


  # population을 shuffle하고, 0번째, 1번째 chromosome 리턴
  def selectTwo(self, pop):
    popCopy = pop[:]
    random.shuffle(popCopy)
    return popCopy[0], popCopy[1]

  
  # fitness 값이 더 작은 chromosome 리턴
  def binaryTournament(self, ind1, ind2):
    if ind1[0] < ind2[0]:
      return ind1
    else:
      return ind2