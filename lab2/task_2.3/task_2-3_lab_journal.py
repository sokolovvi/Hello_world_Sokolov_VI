name = input('Введите ФИО исследователя: ')
date = input('Дата исследования: ')
experiment = input('Введите название эксперимента: ')
conclusion = input('Напишите вывод: ')

with open("journal.txt", "w", encoding="utf-8") as file:
    file.write("Электронный лабораторный журнал:\n\n")
    file.write(f'ФИО исследователя:\t{name}\n')
    file.write(f'Дата:\t\t\t\t{date}\n')
    file.write(f'Эксперимент:\t\t{experiment}\n\n')
    file.write('Вывод:\n')
    file.write(f'{conclusion}')