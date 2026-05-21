import pandas as pd
import numpy as np
import seaborn as sns

# ==============================
# Задание 1.1: 20 бросков кубика
# ==============================
np.random.seed(42)
rolls = np.random.randint(1, 7, size=20)
print("Результаты бросков:", rolls)
mode_rolls = pd.Series(rolls).mode()
print("Мода:", list(mode_rolls))
if len(mode_rolls) == 1:
    print("У набора одна мода")
else:
    print(f"У набора несколько мод ({len(mode_rolls)})")
print("Причина: в случайной выборке может оказаться несколько значений с одинаковой максимальной частотой.\n")

# ==============================
# Задание 1.2: Любимый язык (15 студентов)
# ==============================
np.random.seed(123)
langs = np.random.choice(['Python','Java','C++','JavaScript'], size=15, p=[0.4,0.3,0.2,0.1])
df_lang = pd.DataFrame({'student': range(1,16), 'lang': langs})
print("Распределение языков:\n", df_lang['lang'].value_counts())
mode_lang = df_lang['lang'].mode()
print("Мода:", list(mode_lang))
print("Среднее для номинальных данных вычислить нельзя – они нечисловые и неупорядоченные.\n")

# ==============================
# Задание 1.3: Реальный датасет iris
# ==============================
iris = sns.load_dataset('iris')
print("Датасет iris (первые 5 строк):\n", iris.head())

# Переменная 1: sepal_length
print("\n--- sepal_length ---")
print("Тип данных:", iris['sepal_length'].dtype)
print("Среднее:", iris['sepal_length'].mean())
print("Медиана:", iris['sepal_length'].median())
print("Мода:", iris['sepal_length'].mode().values)

# Переменная 2: petal_length
print("\n--- petal_length ---")
print("Тип данных:", iris['petal_length'].dtype)
print("Среднее:", iris['petal_length'].mean())
print("Медиана:", iris['petal_length'].median())
print("Мода:", iris['petal_length'].mode().values)

# Переменная 3: species (номинальная)
print("\n--- species ---")
print("Тип данных:", iris['species'].dtype)
print("Мода:", iris['species'].mode().values)
print("Среднее и медиана неприменимы (нечисловые данные).")

# Краткие выводы
print("\n=== Выводы ===")
print("1. sepal_length: среднее и медиана близки (≈5.84 и 5.80) – распределение почти симметрично.")
print("2. petal_length: среднее (3.76) и медиана (4.35) различаются – распределение скошено влево/вправо?")
print("   На самом деле из-за разных видов ирисом petal_length имеет два пика, мода = 1.4 (маленькие лепестки).")
print("3. species: все три вида представлены поровну (по 50), поэтому мод три – это показывает, что выборка сбалансирована.")