name = input('Введите имя оператора: ')
sensor_value = input('Введите текущее значение давления (Па): ')

with open("sensor_log.txt", "w", encoding="utf-8") as file:
    file.write(f"Имя оператора: {name}\n")
    file.write(f'Текущее значение давления (Па): {sensor_value}\n')
print('Данные успешно сохранены в sensor_log.txt')
