# Superclass, Parent of 'Problem' & 'HillClimbing'
# Problem 클래스와 HillClimbing 클래스에서 공통적으로 사용하는 것을 
# Setup 클래스로 만듦

class Setup():   
  def __init__(self):
    self._delta = 0.01   # mutation step size
    self._alpha = 0.01   # update rate
    self._dx = 0.0001
   
  def getDelta(self):
    return self._delta

  # Gradient Descent
  def getDx(self):
    return self._dx

  def getAlpha(self):
    return self._alpha
 