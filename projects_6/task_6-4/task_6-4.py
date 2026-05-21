import pandas as pd
import numpy as np

# ============================================================
# ЗАДАНИЕ 1: Время загрузки страниц (среднее и медиана)
# ============================================================
print("=" * 50)
print("ЗАДАНИЕ 1: Время загрузки страниц")
print("=" * 50)

data = [0.8, 1.2, 0.9, 1.5, 1.1, 0.7, 1.3, 12.5, 1.0, 0.9]

# ----- 1а. Ручной расчёт среднего и медианы -----
print("\n--- 1. Ручной расчёт ---")
# Среднее
total = sum(data)
n = len(data)
mean_manual = total / n
print(f"Сумма = {total}, n = {n} -> Среднее = {mean_manual:.2f} сек")

# Медиана
sorted_data = sorted(data)
mid = n // 2
if n % 2 == 0:
    median_manual = (sorted_data[mid-1] + sorted_data[mid]) / 2
else:
    median_manual = sorted_data[mid]
print(f"Отсортированный ряд: {sorted_data}")
print(f"Медиана (n чётное, берём среднее 5-го и 6-го) = {median_manual:.2f} сек")

# ----- 1б. Проверка через pandas -----
df = pd.DataFrame(data, columns=['time'])
print("\n--- 2. Проверка через pandas ---")
print(f"Среднее (pandas): {df['time'].mean():.2f} сек")
print(f"Медиана (pandas): {df['time'].median():.2f} сек")

# ----- 2. Удаление выброса 12.5 -----
print("\n--- 3. После удаления выброса 12.5 ---")
data_clean = [x for x in data if x != 12.5]   # или data[:-1], но так надёжнее
df_clean = pd.DataFrame(data_clean, columns=['time'])
mean_clean = df_clean['time'].mean()
median_clean = df_clean['time'].median()
print(f"Очищенный набор: {data_clean}")
print(f"Среднее: {mean_clean:.2f} сек")
print(f"Медиана: {median_clean:.2f} сек")

# Сравнение
print("\n--- 4. Сравнение исходного и очищенного наборов ---")
print(f"{'Показатель':<12} {'Исходный':<12} {'Очищенный':<12} {'Изменение':<12}")
print(f"{'Среднее':<12} {mean_manual:<12.2f} {mean_clean:<12.2f} {mean_clean - mean_manual:<+12.2f}")
print(f"{'Медиана':<12} {median_manual:<12.2f} {median_clean:<12.2f} {median_clean - median_manual:<+12.2f}")

# ============================================================
# ЗАДАНИЕ 2: DataFrame с выбросами для времени заказов в ресторане
# ============================================================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 2: Время выполнения заказов в ресторане (с выбросами)")
print("=" * 50)

np.random.seed(42)  # для воспроизводимости
# Генерируем 18 нормальных значений (среднее 30 мин, std 5 мин)
normal_times = np.random.normal(30, 5, 18).round(1)
# Добавляем два выброса (аномально долгие заказы)
outliers = [120.0, 150.0]
all_times = np.concatenate([normal_times, outliers])

df_orders = pd.DataFrame(all_times, columns=['time_min'])
print("\nПервые 5 строк + последние 2 (выбросы):")
print(pd.concat([df_orders.head(), df_orders.tail(2)]))

mean_orders = df_orders['time_min'].mean()
median_orders = df_orders['time_min'].median()

print(f"\nСреднее время заказа: {mean_orders:.1f} мин")
print(f"Медиана времени заказа: {median_orders:.1f} мин")

# Подробная статистика для наглядности
print("\n--- Описательная статистика ---")
print(df_orders['time_min'].describe())

# Объяснение разницы
print("\n--- Объяснение ---")
print("Среднее чувствительно к выбросам: два заказа по 120 и 150 мин сильно 'тянут' среднее вверх.")
print(f"Среднее = {mean_orders:.1f} мин, но большинство заказов лежит в районе 30 мин.")
print(f"Медиана = {median_orders:.1f} мин, она игнорирует выбросы и показывает типичное время выполнения.")
print("Поэтому для данных с аномалиями медиана является более устойчивой мерой центральной тенденции.")