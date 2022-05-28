from setup import Setup

class HillClimbing(Setup):
  def __init__(self):       
    super().__init__()  # Setup에 정의된 거 가지고 오기
    self._limitStuck = 100   

  def setVariables(self, aType, pType):
    self._pType = pType
    self._aType = aType  
 
  def displaySetting(self):  # 모든 알고리즘에서 공통적으로 사용되는 정보
    if self._pType == 1 and self._aType != 3:
      print("\nMutation step size:", self.getDelta())
    
  def run(self, p): 
    pass    


class SteepestAscent(HillClimbing):
  def displaySetting(self):  # 추가 설정 출력   # 메서드 오버라이딩
    print("\nSearch Algorithm: SteepestAscent HillClimbing")  
    HillClimbing.displaySetting(self) # 부모 메서드 호출로 공통 부분 출력 
     
  def run(self, p): # 메서드 오버라이딩
    current = p.randomInit() 
    valueC = p.evaluate(current) # 현재 지점 값 계산
    while True:
        neighbors = p.mutants(current)  # 'current' 기준으로 가능한 모든 successor를 구해서 neighbors에 추가
        successor, valueS = self.bestOf(neighbors, p)   # neighbors에서 최적의 것을 successor로 선택
        if valueS >= valueC:    # successor와 current를 비교해서 작은 값을 취함(이동)
            break
        else:      
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)  # 결과 저장

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
  def displaySetting(self):  # 추가 설정 출력 
    print("\nSearch Algorithm: First Choice HillClimbing")  
    print("Limit Stuck: ", self._limitStuck)   
    HillClimbing.displaySetting(self)             
 
  def run(self, p):  # 메서드 오버라이딩
    current = p.randomInit()   # 초기값 랜덤으로 구하기
    valueC = p.evaluate(current)   # current 값 구하기
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
    p.storeResult(current, valueC) # 결과 저장


class gradientDescent(HillClimbing):   
  def displaySetting(self): 
    print("\nSearch Algorithm: Gradient Descent HillClimbing")  
    print("Update rate: ", self.getAlpha())   
    print("Increment for calculating derivatives: ", self.getDx())         
    HillClimbing.displaySetting(self)             

  def run(self, p):  
    current = p.randomInit() # 'current' is a list of values, 초기값 랜덤 설정
    valueC = p.evaluate(current) # current 값 계산
    while True:      
        nextP = p.takeStep(current) # current에서 이동할 next point 구하기
        valueN = p.evaluate(nextP)  # next point에서 값 계산
        if valueN < valueC:                     
            current = nextP               
            valueC = valueN
        else:
            break
    p.storeResult(current, valueC)  # 결과 저장
 

 