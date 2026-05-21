import pandas as pd

# 1. Создаём DataFrame
# Переменные:
# - name — текстовая, не классифицируется для анализа (но можно как номинальную)
# - age — количественная
# - course — порядковая (1 < 2 < 3)
# - python_skill — порядковая (Junior < Middle < Senior)
# - favorite_lang — номинальная (языки без порядка)
# - avg_score — количественная

data = {
    'name': ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий', 
             'Елена', 'Жанна', 'Иван', 'Ксения', 'Леонид'],
    'age': [19, 20, 19, 21, 20, 19, 20, 21, 19, 20],
    'course': [1, 2, 1, 3, 2, 1, 2, 3, 1, 2],
    'python_skill': ['Junior', 'Middle', 'Junior', 'Senior', 'Middle', 
                     'Junior', 'Middle', 'Senior', 'Middle', 'Junior'],
    'favorite_lang': ['Python', 'Java', 'Python', 'C++', 'JavaScript', 
                      'Python', 'Go', 'Python', 'R', 'Swift'],
    'avg_score': [85.5, 72.3, 91.2, 68.7, 79.0, 88.4, 74.6, 93.1, 81.5, 69.8]
}

df = pd.DataFrame(data)

print("Исходный DataFrame:")
print(df)
print("\n")

# 2. Выводим типы данных и поясняем
print("Типы данных столбцов:")
print(df.dtypes)
print("\nПояснение типов:")
print("- name: object (строка) — идентификатор, не используется как переменная для анализа.")
print("- age: int64 — количественная дискретная переменная (возраст в годах).")
print("- course: int64 — по смыслу порядковая (1-й < 2-й < 3-й курс).")
print("- python_skill: object — порядковая переменная (Junior < Middle < Senior).")
print("- favorite_lang: object — номинальная переменная (категории без порядка).")
print("- avg_score: float64 — количественная непрерывная переменная (средний балл).")
print("\n")

# 3. Номинальная переменная: value_counts()
print("Частотное распределение номинальной переменной 'favorite_lang':")
print(df['favorite_lang'].value_counts())
print("\n")

# 4. Порядковая переменная: задаём порядок через pd.Categorical (ordered=True)
skill_order = ['Junior', 'Middle', 'Senior']
df['python_skill_ord'] = pd.Categorical(df['python_skill'], categories=skill_order, ordered=True)

print("Порядковая переменная 'python_skill' после преобразования в категориальную:")
print(df[['name', 'python_skill', 'python_skill_ord']].head())
print("Тип после преобразования:", df['python_skill_ord'].dtype)
print("Порядок категорий:", df['python_skill_ord'].cat.categories)
print("\n")

# Дополнительно: для course тоже зададим порядок (хотя int и так упорядочен, но для демонстрации)
course_order = [1, 2, 3]
df['course_ord'] = pd.Categorical(df['course'], categories=course_order, ordered=True)
print("Курс как порядковая переменная (course_ord):", df['course_ord'].dtype)
print("\n")

# 5. Количественная переменная: describe()
print("Описательная статистика для количественной переменной 'avg_score':")
print(df['avg_score'].describe())
print("\n")

print("Описательная статистика для количественной переменной 'age':")
print(df['age'].describe())