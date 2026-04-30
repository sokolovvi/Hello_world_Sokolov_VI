N = int(input("Введите N: "))

max_val = float(input("Введите число: "))
i = 1
while i <= N:
    if i > max_val:
        max_val = i
    i = i + 1
print(max_val)