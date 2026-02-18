weight = float(input("Введите вес (кг): "))
height = float(input("Введите рост (см): "))

height_m = height / 100
bmi = weight / (height_m ** 2)
print('\n--- Отчет о состоянии здоровья ---\n')
print(f'Рост:\t{height} см')
print(f'Вес:\t{weight} кг')
print(f"Индекс массы тела пациента: {bmi:.2f}")