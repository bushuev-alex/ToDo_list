sum = 0
sum_sq = 0
count = 0
while True:
    number = int(input())
    if count == 0 and number == 0:
        print('0')
        break
    else:
        sum += number
        sum_sq += number**2
        count += 1
        if sum == 0:
            print(sum_sq)
            break
