# "Names.txt" 파일에 입력된 이름들을 가지고와 Set연산을 이용해 집합 만들기
# 만들어진 집합 Set을 반환함

def readSetFromFile():
    infile = open("Names.txt", 'r')
    Set = set()
    for line in infile :
        Set.add(line.rstrip())
    infile.close()
    return Set


# 사용자로부터 이름 입력받기 & 이름 반환

def inputName():
    name = input("Enter a first name to be included: ")
    return name


# 인자로 받은 집합에 이름 추가 & 집합 반환
# 이미 집합에 있는 이름(=파일에 있는 이름)은 중복해서 넣으면 안되므로
# if문으로 중복 검사, 중복되지 않을 시 print문 실행

def insertSet(mySet, name):
    if name not in mySet:
        mySet.add(name)
        print("{} is added in Names.txt" .format(name))
    return mySet

# 새로운 이름을 "Names.txt" 파일에 추가하기 위한 작업
# 이때 파일의 기존 내용은 지우고 수정된 집합을 파일에 쓰는 방식('w').
# 인자로 집합을 받았지만, 파일에 추가할 때는 리스트로 바꿔서 처리한다.
# 알파벳 순서로 넣기 위한 정렬과 개행 문자를 추가한다.
 
def writeToFile(modifiedSet):
    infile = open("Names.txt", "w")
    modifiedSet = list(modifiedSet)
    modifiedSet.sort()

    for item in modifiedSet :
        infile.write(item + "\n")
    infile.close()

    
def main():
    mySet = readSetFromFile()
    name = inputName()
    modifiedSet = insertSet(mySet, name)
    writeToFile(modifiedSet)

main()
