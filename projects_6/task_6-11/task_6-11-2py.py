import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

# ==================================================
# Задание 2.1: Квартили и перцентили для длины крыла пингвинов
# ==================================================
# Загружаем датасет
penguins = sns.load_dataset('penguins')
flipper = penguins['flipper_length_mm'].dropna()   # убираем пропуски

# Вычисляем нужные перцентили
percentiles = [10, 25, 50, 75, 90]
values = [flipper.quantile(p/100) for p in percentiles]

# Таблица с описанием
df_percentiles = pd.DataFrame({
    'Перцентиль': percentiles,
    'Значение (мм)': values,
    'Описание': [
        '10% пингвинов имеют длину крыла ≤ этого значения',
        'Первый квартиль (25%): четверть пингвинов короче',
        'Медиана (50%): центральное значение',
        'Третий квартиль (75%): три четверти пингвинов короче',
        '90% пингвинов имеют длину крыла ≤ этого значения'
    ]
})
print("=== Квартили и перцентили длины крыла (мм) ===")
print(df_percentiles.to_string(index=False))

# Дополнительное пояснение
p10 = values[0]
print(f"\nP10 = {p10:.1f} мм. Это означает, что только 10% пингвинов имеют длину крыла {p10:.1f} мм или меньше, а 90% — длиннее.")

# ==================================================
# Задание 2.2: Перцентиль пингвина Adelie с длиной крыла 190 мм
# ==================================================
print("\n=== Задание 2.2 ===")
adelie_flipper = penguins[penguins['species'] == 'Adelie']['flipper_length_mm'].dropna()
target_length = 190

# Ручной подсчёт: доля Adelie с длиной крыла ≤ 190 мм
count_le = (adelie_flipper <= target_length).sum()
total = len(adelie_flipper)
percentile_manual = (count_le / total) * 100
print(f"Ручной расчёт: {count_le} из {total} пингвинов Adelie имеют длину крыла ≤ {target_length} мм")
print(f"Перцентильный ранг = {percentile_manual:.1f}")

# Через scipy.stats.percentileofscore
percentile_scipy = stats.percentileofscore(adelie_flipper, target_length, kind='weak')
print(f"Через scipy.stats.percentileofscore: {percentile_scipy:.1f}")

# Объяснение
if percentile_manual >= 50:
    print(f"Пингвин с длиной крыла {target_length} мм находится выше медианы своего вида (Adelie).")
else:
    print(f"Пингвин с длиной крыла {target_length} мм находится ниже медианы своего вида (Adelie).")

# ==================================================
# Задание 2.3: Студент с баллом 82 на вступительном экзамене
# ==================================================
print("\n=== Задание 2.3 ===")
np.random.seed(123)
exam_scores = pd.Series(np.random.randint(40, 101, 50))
student_score = 82

# Перцентильный ранг
percentile_rank = (exam_scores <= student_score).mean() * 100
print(f"Результаты экзамена (50 студентов):")
print(f"  Средний балл: {exam_scores.mean():.1f}")
print(f"  Медиана: {exam_scores.median():.1f}")
print(f"  Ваш балл: {student_score}")
print(f"  Перцентильный ранг: {percentile_rank:.1f}")

# Порог приёма — верхние 30% (т.е. балл, выше которого находятся 30% студентов)
# P70 — это 70-й перцентиль: 70% студентов ниже, 30% выше
threshold = exam_scores.quantile(0.70)
print(f"Порог приёма (70-й перцентиль): {threshold:.1f} баллов")

if student_score >= threshold:
    print(f"Студент проходит: его балл {student_score} ≥ {threshold:.1f}.")
else:
    print(f"Студент не проходит: его балл {student_score} < {threshold:.1f}.")

# Альтернативный расчёт: процент студентов, которых он превзошёл
above_percent = (exam_scores > student_score).mean() * 100
print(f"Студент превзошёл {percentile_rank:.1f}% группы, но {above_percent:.1f}% набрали больше.")