from setup import Setup
import random, math


class Optimizer():
  def __init__(self):
    self._pType = 0
    self._aType = 0
    self._numExp = 0

  def setVariables(self, parameters):
    self._pType = parameters['pType']
    self._aType = parameters['aType']   
    self._numExp = parameters['numExp']


  def getAType(self):
    return self._aType

  def getNumExp(self):
    return self._numExp

  def displayNumExp(self):     # Total number of experiments
    print()
    print("Number of experiments: ", self._numExp)

  def displaySetting(self):
    pass  
  


class HillClimbing(Optimizer, Setup):  
  def __init__(self):       
    Optimizer.__init__(self)  
    Setup.__init__(self)
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
    if self._pType == 1 :
      print("Mutation step size:", self._delta)       
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
    f = open('first.txt', 'w')  
    i = 0      
    while i < self._limitStuck:     # current 보다 작은 successor가 없을 때 최대 100번까지만 실행
        successor = p.randomMutant(current)  # 'current'에서 다음으로 이동할 successor 랜덤으로 구하기
        valueS = p.evaluate(successor)       # 'successor'의 값 구하기
        f.write(str(round(valueC, 1))+'\n')     
        if valueS < valueC:         # 최소화를 위해 current보다 successor의 값이 작으면 이동한 뒤 계속 반복
            current = successor                 
            valueC = valueS
            i = 0        # Reset stuck counter
        else:
            i += 1
    f.close()
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
    super().__init__()
    self._numSample = 100           
    self._limitEval = 0
    self._whenBest = 0

  def setVariables(self, parameters):
    super().setVariables(parameters)
    self._limitEval = parameters['limitEval']

  def getWhenBestFound(self):         
    return self._whenBest

  def displaySetting(self):
    pass




class SimulatedAnnealing(MetaHeuristics):
  def displaySetting(self):
    print("\nSearch Algorithm: Simulated Annealing")

  def run(self, p):
    f = open('anneal.txt', 'w')  
    current = p.randomInit()
    valueC = p.evaluate(current)
    t = self.initTemp(p)        # 초기 temperature 구하기
    for i in range(self._limitEval):
        f.write(str(round(valueC, 1))+'\n')              
        nextP = p.randomMutant(current) 
        valueN = p.evaluate(nextP)  
        t = self.tSchedule(t)   # next temperature 구하기
        dE = valueN - valueC    
        if (dE < 0) :                     
          current = nextP               
          valueC = valueN
          self._whenBest = i    # dE < 0 이면 best solution 발생 시점 갱신 
        elif random.uniform(0,1) <= math.exp(-dE/t) :
          current = nextP               
          valueC = valueN  
    f.close()      
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