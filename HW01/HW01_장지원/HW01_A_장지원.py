purchase_price = int(input('Enter purchase price: ')) # 구입 가격을 입력 받고 int형으로 형변환
selling_price = int(input('Enter selling price: '))  # 판매 가격을 입력 받고 int형으로 형변환

markup = 400.0

percentage_markup = markup / purchase_price 
profit_margin = markup / selling_price 

Str = '$' + str(markup) # int형 변수 markup을 str() 함수로 문자열로 변환 

print('Markup:', Str)

# format method를 사용하여 소수점 아래와 '%'를 표현
print('Percentage markup: {0:.1%}' .format(percentage_markup))
print('Profit margin: {0:.2%}'.format(profit_margin))
