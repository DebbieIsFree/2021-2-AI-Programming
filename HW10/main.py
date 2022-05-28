import numpy as np 


def main():
    print()
    print("Which learning algorithm do you want to use?")
    print(" 1. Linear Regression")
    print(" 2. k-NN")

    aType = int(input("Enter the number: "))
    fileName = input("Enter the file name of training data: ")
    fileName = input("Enter the file name of test data: ")

    if aType == 1:
        ml = linearRegression()
    elif aType == 2:
        ml = KNN()

    ml.setData('train', fileName)
    ml.setData('test', fileName)
    ml.buildModel() 
    ml.testModel()
    ml.report()



class ML:
    def __init__(self):
        self._trainDX = np.array([]) # Feature value matrix (training data)
        self._trainDy = np.array([]) # Target column (training data)
        self._testDX = np.array([])  # Feature value matrix (test data)
        self._testDy = np.array([])  # Target column (test data)
        self._testPy = np.array([])  # Predicted values for test data
        self._rmse= 0                # Root mean squared error
        

    def setData(self, dtype, fileName):  # set class variables
        XArray, yArray = self.createMatrices(fileName)
        if dtype == 'train':
            self._trainDX = XArray
            self._trainDy = yArray
        elif dtype == 'test':
            self._testDX = XArray
            self._testDy = yArray
            self._testPy = np.zeros(np.size(yArray))  # Initialize to all 0
            

    def createMatrices(self, fileName):  # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]
            features = data[0:-1]      # 각 줄에서 맨 앞의 data 3개 가져오기
            target = data[-1]          # 각 줄의 맨 마지막 data 가져오기 
            XSet.append(features)       
            ySet.append(target)         
        infile.close()
        XArray = np.array(XSet)      # XSet의 각 element를 array의 한 행으로 만든다.
        yArray = np.array(ySet)
        return XArray, yArray


    # Test with the test set
    def testModel(self):  
        n = np.size(self._testDy)   
        for i in range(n):
            self._testPy[i] = self.runModel(self._testDX[i])  # test data의 예측값 구하기


    # 예측값(testPy)과 실제값(testDy)이 다를 수 있기 때문에 
    # 그 차이(RMSE)를 구해 낮추는게 목표.
    def report(self):
        n = np.size(self._testDy) # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2  # 양수로 만들기, 오차 = (실제값 - 예측값)**2
            totalSe += se
        self._rmse = np.sqrt(totalSe) / n     # 오차 평균 구하기 
        print()
        print("RMSE: ", round(self._rmse, 2))
        



    
class linearRegression(ML):
    def __init__(self):
        ML.__init__(self)
        self._w = np.array([])  # Optimal weights for linear regression


    # Do linear regression and return optimal w
    def buildModel(self):     
        X = self._trainDX
        n = np.size(self._trainDy)  # trainDy 원소 개수만큼
        X0 = np.ones([n, 1])        # 모든 원소가 1인  n행 1열 배열 
        nX = np.hstack((X0, X))     # Add a column of all 1's as the first column
        y = self._trainDy
        t_nX = np.transpose(nX)     # 전치
        self._w =  np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)  


    # Apply linear regression to a test data
    def runModel(self, data):   
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)  # 벡터 내적




class KNN(ML):
    def __init__(self):
        ML.__init__(self)
        self._k = 0        # k value for k-NN
        

    def buildModel(self):  # input k
        self._k = int(input("Enter the value for k: "))
        
    
    def runModel(self, query):    
        closestK = self.findCK(query) # test data와 제일 가까운 training data k개 찾음         
        predict = self.takeAvg(closestK)  # 거리 평균 구하기 
        return predict    # predicted 값을 리턴해서 testPy에 저장.


    # test data와 제일 가까운 train data K개를 구하는 함수  
    def findCK(self, query):
        m = np.size(self._trainDy)  
        k = self._k   
        closestK = np.arange(2 * k).reshape(k,2)  # closestK 설정 (k행, 2열) 
        for i in range(k):     # point별로 거리를 다 비교해서 K개만큼 closestK에 저장
            closestK[i,0] = i  # 인덱스 저장 
            closestK[i,1] = self.sDistance(self._trainDX[i], query)  # 거리 저장
        # k개를 제외한 나머지는 값(거리)을 비교 해가면서 제일 작은 걸로 계속 update
        for i in range(k, m):  
            self.updateCK(closestK, i, query) 
        return closestK


    def updateCK(self, closestK, i, query):  
        d = self.sDistance(self._trainDX[i], query) # trainDx와 testDx(query)의 거리 구하기 
        for j in range(len(closestK)):
            if closestK[j, 1] > d :   # closestK에 저장된 값과 거리 비교해서
                closestK[j, 0] = i    # 새로 구한 거리가 작으면 인덱스와 거리를 바꿈
                closestK[j,1] = d    
                break


    # train data와 test data의 거리를 구함
    def sDistance(self, dataA, dataB):  
        dim = np.size(dataA)    # dimension
        sumOfSquares = 0
        for i in range(dim):   # (a1-b1)**2 + (a2-b2)**2 + (a3-b3)**2
            sumOfSquares += (dataA[i] - dataB[i])**2   
        return sumOfSquares


    def takeAvg(self, closestK): 
        k = self._k
        total = 0
        for i in range(k):
            j = closestK[i,0]          # 인덱스 저장
            total += self._trainDy[j]  # y값 가져오기 
        return total / k       # 제일 가까이 있는 K개의 train data의 y값 평균 




main()
