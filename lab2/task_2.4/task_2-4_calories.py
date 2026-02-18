# Ввод чисел
protein_mass = float(input('Введите массу белков в продукте (г): '))
fat_mass = float(input('Введите массу жиров в продукте (г): '))
carbohydrates_mass = float(input('Введите массу углеводов в продукте (г): '))

# Расчитываем
cal = (protein_mass * 4) + (fat_mass * 9) + (carbohydrates_mass * 4)

print(f'Общая калорийность: {cal}')