import pandas as pd
import numpy as np

# ============================================================
# Задание 1: Анализ переменной с выбросами
# ============================================================
# Создадим свой набор данных (50 значений) с выбросами
np.random.seed(42)
normal = np.random.normal(50, 10, 48)          # 48 нормальных значений
outliers = np.array([120, 5])                  # два явных выброса (очень большой и очень малый)
data = np.concatenate([normal, outliers])
df_raw = pd.DataFrame({'value': data})

print("Исходные данные (первые 5 и последние 5):")
print(pd.concat([df_raw.head(), df_raw.tail()]))

# 1a. Меры разброса до очистки
def spread_measures(series):
    return {
        'Range': series.max() - series.min(),
        'IQR': series.quantile(0.75) - series.quantile(0.25),
        'Var': series.var(),
        'SD': series.std()
    }

before = spread_measures(df_raw['value'])

# 1b. Удаление выбросов методом 1.5×IQR
Q1 = df_raw['value'].quantile(0.25)
Q3 = df_raw['value'].quantile(0.75)
IQR_val = Q3 - Q1
lower = Q1 - 1.5 * IQR_val
upper = Q3 + 1.5 * IQR_val

df_clean = df_raw[(df_raw['value'] >= lower) & (df_raw['value'] <= upper)]
after = spread_measures(df_clean['value'])

# 1c. Таблица сравнения
comparison = pd.DataFrame({
    'Мера': ['Range', 'IQR', 'Var', 'SD'],
    'До очистки': [before['Range'], before['IQR'], before['Var'], before['SD']],
    'После очистки': [after['Range'], after['IQR'], after['Var'], after['SD']]
})
comparison['Изменение, %'] = ((comparison['После очистки'] - comparison['До очистки']) / comparison['До очистки'] * 100).round(2)

print("\n=== Таблица сравнения мер разброса ===")
print(comparison.to_string(index=False))

# ============================================================
# Задание 2: Анализ датасета (аналог 'tips')
# ============================================================
print("\n=== Задание 2 ===")
# Создадим синтетический датасет, похожий на 'tips'
np.random.seed(123)
n = 244  # стандартное количество в tips
total_bill = np.random.gamma(20, 2, n).round(2)  # среднее около 40
tip = (total_bill * np.random.uniform(0.1, 0.3, n)).round(2)
size = np.random.choice([1,2,3,4,5,6], n, p=[0.15,0.3,0.35,0.15,0.04,0.01])

df_tips = pd.DataFrame({
    'total_bill': total_bill,
    'tip': tip,
    'size': size
})
print("Датасет 'tips' (синтетический):")
print(df_tips.head())

# Выбираем числовые переменные
numeric_cols = df_tips.select_dtypes(include=[np.number]).columns
print(f"\nЧисловые переменные: {list(numeric_cols)}")

# Коэффициент вариации (CV = std/mean * 100)
cv_results = {}
for col in numeric_cols:
    mean_val = df_tips[col].mean()
    std_val = df_tips[col].std()
    cv = (std_val / mean_val) * 100
    cv_results[col] = cv
    print(f"{col}: среднее = {mean_val:.2f}, std = {std_val:.2f}, CV = {cv:.2f}%")

# Самая стабильная (наименьший CV) и самая вариативная (наибольший CV)
most_stable = min(cv_results, key=cv_results.get)
most_variable = max(cv_results, key=cv_results.get)
print(f"\nСамая стабильная переменная: {most_stable} (CV = {cv_results[most_stable]:.2f}%)")
print(f"Самая вариативная переменная: {most_variable} (CV = {cv_results[most_variable]:.2f}%)")

print("\nПримечание: CV позволяет сравнивать разброс переменных независимо от их единиц измерения.")
print("В данном случае 'size' (количество гостей) имеет наименьший относительный разброс,")
print("а 'tip' (чаевые) – наибольший, что говорит о высокой вариабельности чаевых относительно среднего.")