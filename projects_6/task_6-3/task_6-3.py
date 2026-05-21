import pandas as pd
import numpy as np

# Фиксируем seed для воспроизводимости
np.random.seed(123)

# 1. Создаём DataFrame с данными о 8 студентах
students = ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий', 'Елена', 'Жанна', 'Иван']
exams = ['Математика', 'Физика', 'Информатика', 'Английский']

# Генерируем случайные оценки от 40 до 100 (целые)
grades = np.random.randint(40, 101, size=(8, 4))

df = pd.DataFrame(grades, index=students, columns=exams)
print("Исходная таблица оценок:")
print(df)

# 2. Вычисляем средний балл каждого студента (по строке)
df['Средний балл студента'] = df.mean(axis=1)
print("\nСредний балл каждого студента:")
print(df['Средний балл студента'])

# Вычисляем средний балл по каждому экзамену (по столбцу)
exam_means = df[exams].mean()
print("\nСредний балл по каждому экзамену (до добавления аномалий):")
print(exam_means)

# 3. Добавляем студента с аномально высоким баллом (100 по всем предметам)
high_anomaly = pd.DataFrame([[100, 100, 100, 100]],
                            index=['Аномально высокий'],
                            columns=exams)
# Добавляем студента с аномально низким баллом (20 по всем)
low_anomaly = pd.DataFrame([[20, 20, 20, 20]],
                           index=['Аномально низкий'],
                           columns=exams)

# Расширяем DataFrame
df_extended = pd.concat([df, high_anomaly, low_anomaly])

# Пересчитываем средний балл студентов (строки)
df_extended['Средний балл студента'] = df_extended[exams].mean(axis=1)

# Пересчитываем средний балл по экзаменам (столбцы)
exam_means_extended = df_extended[exams].mean()

print("\nРасширенная таблица (с аномальными студентами):")
print(df_extended)
print("\nСредний балл по каждому экзамену (после добавления аномалий):")
print(exam_means_extended)

# Дополнительно: сравнение средних до и после
print("\nИзменение средних по экзаменам:")
comparison = pd.DataFrame({'До аномалий': exam_means, 'После аномалий': exam_means_extended})
print(comparison)