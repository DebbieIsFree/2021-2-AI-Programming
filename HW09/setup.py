# Superclass, Parent of 'Problem' & 'Optimizer'
# Problem 클래스와 Optimizeer 클래스에서 공통적으로 사용하는 것

class Setup():   
  def __init__(self):
    self._delta = 0   # mutation step size
    self._alpha = 0   # update rate
    self._dx = 0
    self._aType = 0         
    self._resolution = 0
   
  def getAType(self):
    return self._aType  
  
  def setVariables(self, parameters):             
    self._delta =  parameters['delta']
    self._alpha =  parameters['alpha']
    self._dx = parameters['dx']
    self._aType = parameters['aType']
    self._resolution = parameters['resolution']