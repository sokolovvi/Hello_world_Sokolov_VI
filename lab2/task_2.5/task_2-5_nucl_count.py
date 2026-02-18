print('=== Анализ последовательности ДНК ===\n')
dna = input("Введите последовательность ДНК: ").upper()

# Подсчёт нуклеотидов
count_A = dna.count("A")
count_T = dna.count("T")
count_G = dna.count("G")
count_C = dna.count("C")

# Общая длина последовательности
total = len(dna)

# Процентное содержание каждого нуклеотида
percent_A = count_A / total * 100
percent_T = count_T / total * 100
percent_G = count_G / total * 100
percent_C = count_C / total * 100

print(f'\nПоследовательность в верхнем регистре: {dna}\n')
print('Подсчёт нуклеотидов:')
print(f'А: {count_A}')
print(f'T: {count_T}')
print(f'G: {count_G}')
print(f'C: {count_C}\n')
print('Процентное содержание:')
print(f'A: {percent_A:.2f} %')
print(f'T: {percent_T:.2f} %')
print(f'G: {percent_G:.2f} %')
print(f'C: {percent_C:.2f} %\n')
print(f'Общая длина: {total}')