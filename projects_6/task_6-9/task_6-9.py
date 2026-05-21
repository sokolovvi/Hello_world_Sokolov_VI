import pandas as pd
import numpy as np

# ==================================================
# Задание 1.1: Стандартное отклонение вручную и через pandas
# ==================================================
print("=== Задание 1.1 ===")
data = [2, 3, 2, 4, 3, 5, 2, 3, 4, 3]
s = pd.Series(data)

# Ручной расчёт дисперсии (выборочной)
n = len(data)
mean = sum(data) / n
variance = sum((x - mean)**2 for x in data) / (n - 1)   # деление на n-1 для выборочной
std_manual = variance ** 0.5
print(f"Ручное СО = {std_manual:.4f}")

# Через pandas
std_pandas = s.std()
print(f"pandas .std() = {std_pandas:.4f}")

# Интервал mean ± 1 SD
low = mean - std_manual
high = mean + std_manual
print(f"Интервал mean ± 1 SD: [{low:.2f}, {high:.2f}]")

# Сколько значений попадает внутрь
count_in = sum(1 for x in data if low <= x <= high)
print(f"Значений в интервале: {count_in} из {n} ({count_in/n*100:.1f}%)")

# ==================================================
# Задание 1.2: Два набора с одинаковым средним, разными СО
# ==================================================
print("\n=== Задание 1.2 ===")
np.random.seed(123)
# Набор A: малое СО (стабильный)
mean_val = 50
std_A = 2
data_A = np.random.normal(mean_val, std_A, 1000)
# Набор B: большое СО (в 5 раз больше)
std_B = 10
data_B = np.random.normal(mean_val, std_B, 1000)

# Приводим к одинаковому среднему (округлённо)
mean_A = data_A.mean()
mean_B = data_B.mean()
data_A = data_A - mean_A + mean_val
data_B = data_B - mean_B + mean_val

print(f"Набор A: среднее = {data_A.mean():.2f}, СО = {data_A.std():.2f}")
print(f"Набор B: среднее = {data_B.mean():.2f}, СО = {data_B.std():.2f}")

# Правило двух сигм (mean ± 2*std)
def check_2sigma(data, name):
    mu = data.mean()
    sigma = data.std()
    low = mu - 2*sigma
    high = mu + 2*sigma
    ratio = ((low <= data) & (data <= high)).mean() * 100
    print(f"{name}: {ratio:.1f}% данных в интервале mean±2σ")

check_2sigma(data_A, "Набор A (малое СО)")
check_2sigma(data_B, "Набор B (большое СО)")

print("\nВывод: правило двух сигм точнее работает для набора с меньшим разбросом,")
print("потому что такие данные чаще приближены к нормальному распределению.")
print("При большом разбросе могут появляться выбросы, искажающие процентили.")

# ==================================================
# Задание 1.3: Коэффициент вариации для трёх переменных
# ==================================================
print("\n=== Задание 1.3 ===")
# Примеры данных из разных областей
prices_rub = [150, 230, 310, 90, 470, 520, 290, 380, 210, 440]      # цены в рублях
height_cm = [165, 172, 168, 180, 158, 175, 182, 169, 171, 177]      # рост в см
exam_scores = [65, 72, 68, 70, 75, 71, 69, 73, 74, 70]              # баллы (0-100)

df_vars = pd.DataFrame({
    'Цена (руб)': prices_rub,
    'Рост (см)': height_cm,
    'Баллы': exam_scores
})

print("Исходные данные:")
print(df_vars.head())

def cv(series):
    """Коэффициент вариации = std / mean (в процентах)"""
    return (series.std() / series.mean()) * 100

for col in df_vars.columns:
    mean_val = df_vars[col].mean()
    std_val = df_vars[col].std()
    cv_val = cv(df_vars[col])
    print(f"\n{col}:")
    print(f"  среднее = {mean_val:.2f}, СО = {std_val:.2f}")
    print(f"  CV = {cv_val:.1f}%")

max_cv = max([cv(df_vars[col]) for col in df_vars.columns])
print(f"\nНаибольший относительный разброс ({max_cv:.1f}%) – у цен в рублях.")
print("Это говорит о том, что цены товаров варьируются сильнее относительно своего среднего,")
print("чем рост людей или экзаменационные баллы. Такой показатель полезен для сравнения")
print("вариативности величин, измеряемых в разных единицах.")