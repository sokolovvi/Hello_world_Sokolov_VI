N = int(input("Введите N: "))

sum_val = 0
i = 1
while i <= N:
    sum_val = sum_val + i
    i = i + 1
avg = sum_val / N
print(avg)