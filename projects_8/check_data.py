import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port='5430',
    user='postgres_user',
    password='postgres_password',
    database='postgres_db'
)

cursor = conn.cursor()

# Проверяем оценки
cursor.execute("SELECT COUNT(*) FROM enrollments WHERE grade IS NOT NULL;")
count = cursor.fetchone()[0]
print(f"Количество оценок в БД: {count}")

# Показываем несколько оценок
cursor.execute("SELECT grade FROM enrollments WHERE grade IS NOT NULL LIMIT 10;")
grades = cursor.fetchall()
print("Примеры оценок:", [g[0] for g in grades])

cursor.close()
conn.close()