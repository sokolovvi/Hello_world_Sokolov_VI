# 1. ВВОД ДАННЫХ
environment_name = input('Введите название питательной среды: ')
agar_concentration = input('Введите концентрацию агара (%): ')
temperature = input('Введите температуру стерилизации (°C): ')

# 2. РАБОТА С ФАЙЛОМ
with open("recipe.txt", "w", encoding="utf-8") as report:
    # 3. ЗАПИСЬ И ФОРМАТИРОВАНИЕ
    report.write(f"Название питательной среды: {environment_name}\n")
    report.write(f"Концентрация агара (%): {agar_concentration}\n")
    report.write(f"Температура стерилизации (°C): {temperature}\n")
print("Файл 'recipe.txt' успешно сформирован!")