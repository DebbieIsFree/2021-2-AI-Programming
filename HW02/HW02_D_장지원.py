

# 월이자 (intForMonth) : 월이율 * 매 시작 달의 대출금 잔액(begBalance)
# 매달 상환액 (redOfPrincipal) : 매달 납부액(monthlyPayment) - 월이자(intForMonth)
# 대출금 잔액 (endBalance) : 대출 원금(begBalance) - 매달 상환액(redOfPrincipal)

# 위의 값을 구해 튜플 형태로 반환함

def calculateValues(annualRateOfInterest, monthlyPayment, begBalance):
    intForMonth = (annualRateOfInterest / 100)/ 12 * begBalance
    redOfPrincipal = monthlyPayment - intForMonth
    endBalance = begBalance - redOfPrincipal

    return (intForMonth, redOfPrincipal, endBalance)




# 연이율, 매달 납부액, 대출 원금 입력받기

annualRateOfInterest = float(input("annual rate of interest: "))
monthlyPayment = float(input("Enter monthly payment: "))
begBalance = float(input("Enter beg. of month balance: "))


# 위에 정의한 calculateValues 함수에 인자(연이율, 매달 납부액, 대출 원금)를 주고 호출하여
# 이자, 매달 납부액에서 이자를 뺀 값 (매달 상환액), 대출 잔액 (intForMonth, redOfPrincipal, endBalance)을
# 튜플 형태로 구하기

(intForMonth, redOfPrincipal, endBalance) = calculateValues(annualRateOfInterest, monthlyPayment, begBalance)


# format method를 사용하여 ','로 3자리 구분 및 소수점 아래 2자리 출력

print("Interest paid for the month: ${:,.2f}" .format(intForMonth))
print("Reduction of principal: ${:,.2f}" .format(redOfPrincipal))
print("End of month balance: ${:,.2f}" .format(endBalance))
