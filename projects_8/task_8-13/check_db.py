import psycopg2

# Ваши параметры подключения
conn = psycopg2.connect(
    host='localhost',
    port='5430',
    user='postgres_user',
    password='postgres_password',
    database='postgres_db'
)

cursor = conn.cursor()

# Показать все таблицы
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

print("Таблицы в базе данных:")
for table in cursor.fetchall():
    print(f"  - {table[0]}")

# Для каждой таблицы показать столбцы
cursor.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
""")

print("\nСтолбцы в таблицах:")
current_table = None
for table, column, data_type in cursor.fetchall():
    if table != current_table:
        print(f"\n  Таблица: {table}")
        current_table = table
    print(f"    - {column} ({data_type})")

cursor.close()
conn.close()