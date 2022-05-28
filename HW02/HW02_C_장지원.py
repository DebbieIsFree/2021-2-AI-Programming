new = []
encoded_list = []
prev =  0
count = 0

# 리스트 형태로 문자열 입력받기
data = input("Input list = ")


# 입력받은 문자열에서 '[', ']', ',', ' '를 제외한 문자를
# 정수값으로 변환하여 new 리스트에 추가하기

for i in range(len(data)):
    if data[i] == '[' or data[i] == ']' or data[i] == ',' or data[i] == ' ':
        continue
    new.append(ord(data[i]) - 48)

   
# [숫자, 빈도]를 구하기 위해 정렬
new.sort()



# 이전 값과 같으면 count 값 증가
# 같지 않으면 [이전 값, count]를 encoded_list에 추가

for i in new:
    if prev == i:
        count += 1 
    else :
        encoded_list.append([prev, count])
        prev = i
        count = 1
        if(i == new[-1]):   # 마지막 원소 처리
            encoded_list.append([prev, count])
            

# 0 ~ 9 중에서 입력받지 못한 값은 빈도를 0으로 하여 추가

for i in range(1, 10):
    if i not in new:
        encoded_list.append([i,0])


# 차례대로 출력하기 위해 정렬
encoded_list.sort()

print("Encoded list = {}".format(encoded_list))

# [4, 2, 5, 2, 5, 5, 1, 2, 6, 8, 9]
