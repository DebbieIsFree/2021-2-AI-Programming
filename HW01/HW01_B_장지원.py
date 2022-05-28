# salary 값을 문자열로 입력받아 int형으로 형변환
salary = int(input('Enter beginning salary: '))

# new_salary = salary * ((1 + 0.1)**3)
new_salary = salary * pow(1.1, 3)

# format method로 소수점 아래 2자리 실수를 ,로 구분해서 표시
print('New salary: ' + '$' + '{0:,.2f}' .format(new_salary))

change = (new_salary - salary) / salary

# 소수점 아래 2자리까지를 백분율 %로 표
print('Change: {0:.2%}'.format(change))
