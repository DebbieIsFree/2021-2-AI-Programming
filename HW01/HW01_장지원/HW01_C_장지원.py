# 1부터 100만까지 숫자의 각 자리수 더하기

total_sum = 0


for i in range(1, 1000001):     # i : 1 ~ 10^6까지 숫자가 주어지고
    for j in str(i):         # j : i를 string형으로 변환해
        total_sum  += int(j) # 문자열(j)의 첫 인덱스부터 끝까지 돌며 int형으로 변환해
                             # 각 자리의 숫자를 더한다.
         

print('The sum of digits in the numbers')


print('from 1 to one million is {:,}.' .format(total_sum))
