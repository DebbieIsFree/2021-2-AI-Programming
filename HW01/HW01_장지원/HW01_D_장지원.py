
# 계수를 입력받고 float로 형변환
coefficient = float(input('Enter coefficient of restitution: '))

# 초기 높이를 입력받고 int로 형변환
initial_height = int(input('Enter initial height in meters: '))

meters = initial_height
total = initial_height # 초기 높이에서 내려오므로 이 값을 더함

bounce = 0

while True :
    bounce += 1
    meters = meters * coefficient # 이전 높이에 계수를 곱해 갱신함
    if meters < 0.10 :  # 높이가 10cm보다 낮으면 멈춘다
        break
    total += meters * 2 # 올라갔다 내려오므로 2배
   
print('Number of bounces:', bounce)
print('Meters traveled: {:.2f}' .format(total))
