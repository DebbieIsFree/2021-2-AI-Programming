
import random


# Human과 Computer를 subclass로 갖는 클래스
class Contestant:

    # instance 변수인 이름과 점수를 초기화 하는 생성
    def __init__(self, name="", score=0):
        self._name = name
        self._score = score

    #각각 객체의 name과 score 변수의  값을 얻는 accessor 메서드
    def getName(self):
        return self._name

    def getScore(self):
        return self._score

    # 게임에서 이기면 객체의 점수를 증가시키는 메서드
    def incrementScore(self):
        self._score += 1



# Contestant의 subclass
class Human(Contestant):

    # 사람으로부터 "가위, 바위, 보"를 입력받고
    # 그 외 값을 입력받았으면 유효한 값을 입력받을 때까지 반복
    def makeChoice(self):
        option = ["rock", "scissors", "paper"]
        hChoice = input("{}, enter your choice: ".format(self._name))
        
        while (hChoice not in option) :
              hChoice = input("{}, enter your choice: ".format(self._name))

        return hChoice


# Contestant의 subclass
class Computer(Contestant):

    # 컴퓨터의 선택을 무작위로 결정하는 메서드
    def makeChoice(self):
        option = ["rock", "scissors", "paper"]
        cChoice = random.choice(option)
        print("{0} chooses {1}".format(self._name, cChoice))
        return cChoice
    

        

# 가위, 바위, 보 게임을 3번 반복
# 이기는 사람의 점수를 각 객체의 incrementScore() 메서드를 호출해 증가시킴
def playGames(h, c):
    for i in range(3):
        choiceH = h.makeChoice()
        choiceC = c.makeChoice()

        if choiceH == choiceC :
            pass
        elif higher(choiceH, choiceC):
            h.incrementScore()
        else :
            c.incrementScore()
        print(h.getName() + ":", h.getScore(),
              c.getName() + ":", c.getScore())
        print()


# 게임에서 승부를 가르기 위한 함수
def higher(c1, c2):
    if ((c1 == 'rock' and c2 == 'scissors') or
        (c1 == 'paper' and c2 == 'rock') or
        (c1 == 'scissors' and c2 == 'paper')):
        return True
    else :
        return False


def main():
    # 사람과 컴퓨터의 이름을 입력받아, 각각의 객체를 생성
    
    Hname = input("Enter name of human: ")
    Cname = input("Enter name of computer: ")
    print()

    human = Human(Hname)
    computer = Computer(Cname)
    
    # 생성된 객체를 인자로 전달해 게임 시작
    playGames(human, computer)


    # 무승부이면 "TIE"를 출력하고, 아니면 점수가 높은 쪽에 "WINS"를 출력한다.
    if human.getScore() == computer.getScore() :
        print("TIE")
    elif human.getScore() > computer.getScore() :
        print("{} WINS".format(human.getName()))
    else :
        print("{} WINS".format(computer.getName()))    
    
    

main()


















