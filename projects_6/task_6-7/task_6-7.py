import pandas as pd
import numpy as np

# ==================================================
# Задание 1.1: Range и IQR вручную + проверка pandas
# ==================================================
print("=== Задание 1.1 ===")
data = [55, 60, 62, 65, 67, 70, 72, 74, 75, 78, 80, 82, 98]
s = pd.Series(data)

# Ручной расчёт
sorted_data = sorted(data)
n = len(data)
range_manual = max(data) - min(data)

# Квартили
pos_q1 = 0.25 * (n + 1)  # 3.5
q1_manual = (sorted_data[2] + sorted_data[3]) / 2  # 3-й и 4-й индексы (0-based)
pos_q3 = 0.75 * (n + 1)  # 10.5
q3_manual = (sorted_data[9] + sorted_data[10]) / 2
iqr_manual = q3_manual - q1_manual

print("Ручной расчёт:")
print(f"  Range = max({max(data)}) - min({min(data)}) = {range_manual}")
print(f"  Q1 = {q1_manual}, Q3 = {q3_manual}, IQR = {iqr_manual}")

# Проверка pandas
print("\nПроверка через pandas:")
print(f"  Range: {s.max() - s.min()}")
print(f"  IQR: {s.quantile(0.75) - s.quantile(0.25)}")

# ==================================================
# Задание 1.2: Поиск выбросов методом 1.5×IQR
# ==================================================
print("\n=== Задание 1.2 ===")
lower_bound = q1_manual - 1.5 * iqr_manual
upper_bound = q3_manual + 1.5 * iqr_manual
print(f"Границы: [{lower_bound}, {upper_bound}]")
outliers = [x for x in data if x < lower_bound or x > upper_bound]
print(f"Выбросы: {outliers if outliers else 'нет'}")

# Среднее исходное и после удаления (хотя выбросов нет)
mean_original = s.mean()
mean_clean = mean_original  # так как нет выбросов
print(f"Среднее исходное: {mean_original:.2f}")
print(f"Среднее после удаления выбросов: {mean_clean:.2f}")

# ==================================================
# Задание 1.3: DataFrame с ценами, удаление выбросов
# ==================================================
print("\n=== Задание 1.3 ===")
np.random.seed(42)
normal_prices = np.random.randint(500, 1500, 13)
outliers_prices = [10, 5000]   # очень дешёвый и очень дорогой
prices_all = np.concatenate([normal_prices, outliers_prices])
df_shop = pd.DataFrame({'price': prices_all})

print("Исходные цены (15 товаров):")
print(df_shop['price'].values)

Q1 = df_shop['price'].quantile(0.25)
Q3 = df_shop['price'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outlier_mask = (df_shop['price'] < lower) | (df_shop['price'] > upper)
print(f"\nQ1 = {Q1:.2f}, Q3 = {Q3:.2f}, IQR = {IQR:.2f}")
print(f"Границы для выбросов: [{lower:.2f}, {upper:.2f}]")
print("Обнаруженные выбросы:")
print(df_shop[outlier_mask])

df_clean_shop = df_shop[~outlier_mask]
mean_before = df_shop['price'].mean()
mean_after = df_clean_shop['price'].mean()

print(f"\nСредняя цена ДО удаления выбросов: {mean_before:.2f}")
print(f"Средняя цена ПОСЛЕ удаления выбросов: {mean_after:.2f}")
print(f"Изменение: {mean_after - mean_before:.2f} ({(mean_after/mean_before - 1)*100:.1f}%)")