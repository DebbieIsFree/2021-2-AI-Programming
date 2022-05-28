
# 리스트 형태로 문자열 입력받기
s = input("Enter a number as list : ")

data = []

# 문자열 안에서 0~9에 해당하는 값만 data 리스트에 추가
for i in range(len(s)):
    if s[i].isdigit() == True:
        data.append(int(s[i]))


# 중간값을 구하기 위해 전체 데이터를 정렬 
data.sort()     


# 전체 데이터 개수
N = len(data)    


# 원소 개수가 짝수 : N/2번째와 (N/2)-1번째 값의 평균 출력
if N % 2 == 0:
    avg = (data[N // 2] + data[N//2 -1]) / 2 
    print("Median: {:.1f}" .format(avg))

 # 원소 개수가 홀수: (전체 개수 // 2)번째 값 출력
else : 
    print("Median: {:.1f}" .format(data[N//2]))
    



