import pandas as pd
import numpy as np

# ==================================================
# Задание 1.1: Квартили вручную и через pandas
# ==================================================
print("=== Задание 1.1 ===")
data = [12, 18, 15, 22, 14, 35, 19, 16, 28, 11, 42, 17]
sorted_data = sorted(data)
n = len(sorted_data)
print(f"Отсортированный ряд: {sorted_data}")
print(f"Количество элементов n = {n}")

# Ручной расчёт
# Q2 (медиана) – для чётного n: среднее двух центральных
pos1 = n // 2 - 1   # 5-й элемент (индекс 5, значение 17)
pos2 = n // 2       # 6-й элемент (индекс 6, значение 18)
q2_manual = (sorted_data[pos1] + sorted_data[pos2]) / 2
print(f"Q2 (медиана): ({sorted_data[pos1]} + {sorted_data[pos2]})/2 = {q2_manual}")

# Q1 – медиана нижней половины (первые 6 элементов)
lower_half = sorted_data[:n//2]   # первые 6: [11,12,14,15,16,17]
m = len(lower_half)
if m % 2 == 0:
    q1_manual = (lower_half[m//2 - 1] + lower_half[m//2]) / 2
else:
    q1_manual = lower_half[m//2]
print(f"Нижняя половина: {lower_half}")
print(f"Q1: {q1_manual}")

# Q3 – медиана верхней половины (последние 6 элементов)
upper_half = sorted_data[n//2:]   # последние 6: [18,19,22,28,35,42]
if len(upper_half) % 2 == 0:
    q3_manual = (upper_half[m//2 - 1] + upper_half[m//2]) / 2
else:
    q3_manual = upper_half[m//2]
print(f"Верхняя половина: {upper_half}")
print(f"Q3: {q3_manual}")

# Проверка через pandas
s = pd.Series(data)
print("\nПроверка через pandas:")
print(f"Q1 = {s.quantile(0.25)}")
print(f"Q2 = {s.quantile(0.5)}")
print(f"Q3 = {s.quantile(0.75)}")

# ==================================================
# Задание 1.2: Датасет 'tips' (чаевые)
# ==================================================
# Для работы требуется seaborn. Если его нет, можно использовать встроенный датасет из библиотеки.
# Альтернативно – загрузить данные из открытого источника, но здесь мы используем seaborn.
try:
    import seaborn as sns
    df = sns.load_dataset('tips')
except ImportError:
    print("Seaborn не установлен. Создаём синтетический датасет, аналогичный 'tips'.")
    np.random.seed(123)
    n = 244
    total_bill = np.random.gamma(20, 2, n).round(2)
    tip = (total_bill * np.random.uniform(0.1, 0.3, n)).round(2)
    df = pd.DataFrame({'total_bill': total_bill, 'tip': tip})

print("\n=== Задание 1.2 ===")
print("Первые 5 строк датасета:")
print(df.head())

# Квартили для total_bill
Q1_tot = df['total_bill'].quantile(0.25)
Q2_tot = df['total_bill'].quantile(0.50)
Q3_tot = df['total_bill'].quantile(0.75)
print(f"\nКвартили total_bill: Q1={Q1_tot:.2f}, Q2={Q2_tot:.2f}, Q3={Q3_tot:.2f}")

# Разбиваем на 4 группы
def assign_quartile(value):
    if value <= Q1_tot:
        return 1
    elif value <= Q2_tot:
        return 2
    elif value <= Q3_tot:
        return 3
    else:
        return 4

df['quartile_group'] = df['total_bill'].apply(assign_quartile)

# Средняя сумма чаевых в каждой группе
avg_tip_by_group = df.groupby('quartile_group')['tip'].mean().round(2)
print("\nСредняя сумма чаевых по квартильным группам (total_bill):")
for group in [1,2,3,4]:
    print(f"Группа {group} (нижняя -> верхняя): {avg_tip_by_group[group]} $")