
# "Units.txt" 파일로부터 딕셔너리 만들기
# 딕셔너리를 선언하고
# 파일에서 한줄씩 읽어들인 값을 ','로 구분해
# 각각 딕셔너리의 key값과 value값으로 준다.
# (value값은 계산을위해 float형으로 바꿈)

def populateDictionary():
    infile = open("Units.txt" , 'r')
    dictionary = dict()

    for line in infile :
        data = line.split(',')
        dictionary[data[0]] = float(data[1].rstrip())
        
    return dictionary
    
# 사용자로부터 단위와 길이 입력받기
# 길이는 계산을 위해 float형으로 바꿈
# 기존 단위, 바꿀 단위, 길이를 튜플 형태로 반환

def getInput():
    orig = input("Unit to convert from: ")
    dest = input("Unit to convert to: ")
    length = float(input("Enter length in yards: "))
    return (orig, dest, length)


def main():
    # 함수 호출로 반환된 값을 변수에 저장
    feet = populateDictionary()
    orig, dest, length = getInput()

    # 딕셔너리에서 key값이 각각 orig와 dest인 요소의 value값으로 계산
    ans = length * feet[orig] / feet[dest]    
    print("Length in {0}s: {1:,.4f}" .format(dest, ans))



main()
