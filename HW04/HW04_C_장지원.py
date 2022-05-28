
# 6개의 퀴즈 점수에 대한 변수와 메소드를 관리하기 위한 클래스

class Quizzes:

    # 생성자 : 인자로 받은 값으로 초기화 한다.
    def __init__(self, listOfGrades):
        self._listOfGrades = listOfGrades


    # 최하위 점수 1개를 제외한 5개의 점수의 평균을 구하는 메서드
    def average(self):
        sum = 0
        lowestGrade = min(self._listOfGrades)
        
        for i in self._listOfGrades:
            sum += i
        average = (sum - lowestGrade) / 5

        return average

    
    # 객체의 현재 상태를 출력하는 메서드
    # __str__ 메서드 안에서 다시 average 메서드를 호출한다.
    def __str__(self):
        return ("Quiz average: " + str(self.average()))
        



def main():
    # 6개의 퀴즈에 대해 0 ~ 10 사이의 점수를 입력받고 리스트에 저장한다. 

    listOfGrades = []

    for i in range(6):
        grade = float(input("Enter grade on quiz {}: ".format(i+1)))
        listOfGrades.append(grade)


    # Quizzes 클래스의 객체 q를 만들기 위해,
    # 리스트 listOfGrades를 인자로 전달해 생성자(__init__)를 호출한다.
    q = Quizzes(listOfGrades)
    

    # 객체 q의 __str__메서드를 호출해 객체의 현재 상태를 출력한다.
    print(q)



main()
