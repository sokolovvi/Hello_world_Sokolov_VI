# check_prices_data.py
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port='5430',
    user='postgres_user',
    password='postgres_password',
    database='postgres_db'
)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM prices;")
count = cursor.fetchone()[0]
print(f"Количество записей в таблице prices: {count}")

cursor.execute("SELECT COUNT(*) FROM products;")
count2 = cursor.fetchone()[0]
print(f"Количество записей в таблице products: {count2}")

cursor.execute("""
    SELECT p.name, p.category, pr.price 
    FROM products p 
    JOIN prices pr ON p.id = pr.product_id 
    LIMIT 5;
""")
print("\nПримеры данных:")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}): {row[2]} руб.")

cursor.close()
conn.close()