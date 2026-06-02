import psycopg2

# Подключение к БД
conn = psycopg2.connect(
    host='localhost',
    port='5430',
    user='postgres_user',
    password='postgres_password',
    database='postgres_db'
)

cursor = conn.cursor()

# 1. Добавляем студентов
print("Добавляем студентов...")
cursor.execute("""
    INSERT INTO students (student_id, first_name, last_name, email, enrollment_year) VALUES
    (1, 'Иван', 'Петров', 'ivan@email.com', 2023),
    (2, 'Мария', 'Сидорова', 'maria@email.com', 2023),
    (3, 'Алексей', 'Иванов', 'alex@email.com', 2024),
    (4, 'Елена', 'Козлова', 'elena@email.com', 2024),
    (5, 'Дмитрий', 'Соколов', 'dmitry@email.com', 2023),
    (6, 'Анна', 'Волкова', 'anna@email.com', 2024)
    ON CONFLICT (student_id) DO NOTHING;
""")

# 2. Добавляем курсы
print("Добавляем курсы...")
cursor.execute("""
    INSERT INTO courses (course_id, course_name, credits) VALUES
    (1, 'Математика', 5),
    (2, 'Физика', 4),
    (3, 'Программирование', 6),
    (4, 'Базы данных', 5),
    (5, 'Веб-разработка', 4)
    ON CONFLICT (course_id) DO NOTHING;
""")

# 3. Добавляем оценки (enrollments)
print("Добавляем оценки...")
cursor.execute("""
    INSERT INTO enrollments (enrollment_id, student_id, course_id, grade) VALUES
    (1, 1, 1, 85), (2, 1, 2, 90), (3, 1, 3, 88),
    (4, 2, 1, 75), (5, 2, 3, 92), (6, 2, 4, 86),
    (7, 3, 2, 78), (8, 3, 4, 95), (9, 3, 5, 89),
    (10, 4, 1, 82), (11, 4, 3, 91), (12, 4, 5, 87),
    (13, 5, 2, 88), (14, 5, 4, 93), (15, 5, 1, 79),
    (16, 6, 3, 94), (17, 6, 4, 88), (18, 6, 5, 90),
    (19, 1, 4, 87), (20, 2, 5, 84), (21, 3, 1, 91),
    (22, 4, 2, 79), (23, 5, 3, 86), (24, 6, 1, 93)
    ON CONFLICT (enrollment_id) DO NOTHING;
""")

conn.commit()

# Проверяем, что данные добавились
cursor.execute("SELECT COUNT(*) FROM enrollments WHERE grade IS NOT NULL;")
count = cursor.fetchone()[0]
print(f"\n✅ Успешно добавлено! Теперь в БД {count} оценок.")

# Показываем примеры
cursor.execute("""
    SELECT s.first_name, s.last_name, c.course_name, e.grade
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    LIMIT 5;
""")

print("\nПримеры добавленных оценок:")
for row in cursor.fetchall():
    print(f"  {row[0]} {row[1]} - {row[2]}: {row[3]}")

cursor.close()
conn.close()

print("\n🎉 Готово! Теперь перезапустите Flask и проверьте кнопки!")