import pandas as pd
import numpy as np

# Устанавливаем seed для воспроизводимости
np.random.seed(42)

# 1. Создаём генеральную совокупность (500 записей)
n_pop = 500
categories = ['Электроника', 'Одежда', 'Книги', 'Дом и сад', 'Спорт']
ratings = [1, 2, 3, 4, 5]

data = {
    'price': np.random.uniform(500, 15000, n_pop).round(2),   # непрерывная, цена от 500 до 15000 руб.
    'reviews_count': np.random.poisson(lam=50, size=n_pop),    # дискретная, количество отзывов
    'category': np.random.choice(categories, n_pop),           # номинальная
    'rating': np.random.choice(ratings, n_pop, p=[0.05, 0.10, 0.20, 0.35, 0.30])  # порядковая (1-5)
}

df_pop = pd.DataFrame(data)

# Параметр генеральной совокупности (средняя цена)
mu = df_pop['price'].mean()
print(f"Генеральная средняя цена (μ) = {mu:.2f} руб.\n")

# 2. Формируем три выборки разного размера
sample_sizes = [20, 50, 100]
samples = {}
for n in sample_sizes:
    samples[n] = df_pop.sample(n, random_state=42)  # фиксируем random_state для воспроизводимости

# 3. Вычисляем средние для каждой выборки и ошибку
results = []
for n in sample_sizes:
    sample_mean = samples[n]['price'].mean()
    error = abs(sample_mean - mu)  # абсолютная ошибка
    results.append({
        'Размер выборки': n,
        'Среднее (выборка)': round(sample_mean, 2),
        'Параметр (μ)': round(mu, 2),
        'Ошибка': round(error, 2)
    })

df_results = pd.DataFrame(results)

print("Результаты сравнения:")
print(df_results.to_string(index=False))