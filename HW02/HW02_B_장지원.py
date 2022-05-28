
# 리스트의 reverse()와 join() method를 사용하기 위해
# 각 자리의 숫자를 문자열로 저장
lst = ['2', '1', '7', '8']

# 4 * abcd = dcba가 되는 숫자(abcd)를 구하기 위해 join()을 사용
abcd = int(''.join(lst))   

# dcba를 구하기 위해 리스트를 거꾸로 뒤집기
lst.reverse()

# 거꾸로 뒤집은 리스트에 join()을 사용해 dcba 구하기
dcba = int(''.join(lst))


print("Since 4 x {0} is {1}," .format(abcd, dcba))
print("the special number is {}" .format(dcba))





