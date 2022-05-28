
# (m <= n)인 두 수를 입력받아, m부터 n까지의 수를 출력하는 재귀함수
# (m <= n)이면, m을 출력하고 (m+1, n)을 인자로 함수 호출
# (m == n)이면, 탈출조건이므로 함수 종료

def displaySequenceNumbers(m, n):
    if m == n :
        return m
    elif m < n :
        print(m)   
        return displaySequenceNumbers(m+1, n)
        
    

def main():
    print("output of print (displaySequenceNumbers(2,4))")
    print(displaySequenceNumbers(2,4))

    print("output of print (displaySequenceNumbers(3,3))")
    print(displaySequenceNumbers(3,3))



main()


