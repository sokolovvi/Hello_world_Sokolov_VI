import psycopg2
from collections import defaultdict
import statistics

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5430",
        user="postgres_user",
        password="postgres_password",
        database="postgres_db"
    )
    print("✓ Подключение к базе данных установлено.\n")

    cursor = connection.cursor()

    query = """
        SELECT
            p.name AS product_name,
            p.category,
            pr.price
        FROM products p
        JOIN prices pr ON p.id = pr.product_id
        ORDER BY p.category, p.name;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("❌ Нет данных в таблицах! Добавьте тестовые данные.")
        exit()

    prices = []
    products_data = []

    for row in rows:
        product_name, category, price = row
        prices.append(price)
        products_data.append((product_name, category, price))

    print(f"=== Данные загружены ===")
    print(f"Всего записей о ценах: {len(prices)}")
    print(f"Уникальных товаров: {len(set(row[0] for row in products_data))}")
    print(f"Категорий: {len(set(row[1] for row in products_data))}\n")

    print("=== 3. Основная статистика по ценам (в рублях) ===")
    mean_val = statistics.mean(prices)
    median_val = statistics.median(prices)
    std_val = statistics.stdev(prices) if len(prices) > 1 else 0
    min_val = min(prices)
    max_val = max(prices)

    print(f"Среднее значение: {mean_val:.2f} руб.")
    print(f"Медиана: {median_val:.2f} руб.")
    print(f"Стандартное отклонение: {std_val:.2f} руб.")
    print(f"Минимальная цена: {min_val:.2f} руб.")
    print(f"Максимальная цена: {max_val:.2f} руб.\n")

    print("=== 4. Квартили и товары с ценой выше Q3 ===")
    sorted_prices = sorted(prices)
    n = len(sorted_prices)

    q1 = sorted_prices[int(n * 0.25)]
    q2 = sorted_prices[int(n * 0.50)]
    q3 = sorted_prices[int(n * 0.75)]
    iqr = q3 - q1

    print(f"Q1 (25-й перцентиль): {q1:.2f} руб.")
    print(f"Q2 (Медиана, 50-й): {q2:.2f} руб.")
    print(f"Q3 (75-й перцентиль): {q3:.2f} руб.")
    print(f"Межквартильный размах (IQR): {iqr:.2f} руб.")

    expensive_items = [(name, cat, price) for name, cat, price in products_data if price > q3]
    print(f"\nТовары, цена которых превышает {q3:.2f} руб. (Q3):")
    if expensive_items:
        for name, cat, price in expensive_items:
            print(f"  {name} ({cat}): {price:.2f} руб.")
    else:
        print("  Таких товаров нет.")
    print()

    print("=== 5. Статистика по категориям (сортировка по убыванию средней цены) ===")

    categories_data = defaultdict(list)
    for name, cat, price in products_data:
        categories_data[cat].append(price)

    category_stats = []
    for cat, prices_list in categories_data.items():
        cat_mean = statistics.mean(prices_list)
        cat_median = statistics.median(prices_list)
        cat_std = statistics.stdev(prices_list) if len(prices_list) > 1 else 0
        cat_count = len(prices_list)
        category_stats.append((cat, cat_count, cat_mean, cat_median, cat_std))

    category_stats.sort(key=lambda x: x[2], reverse=True)

    print(f"{'Категория':<20} {'Кол-во':<8} {'Средняя':<12} {'Медиана':<12} {'Ст. отклонение':<15}")
    print("-" * 70)
    for cat, count, mean_val, median_val, std_val in category_stats:
        print(f"{cat:<20} {count:<8} {mean_val:<12.2f} {median_val:<12.2f} {std_val:<15.2f}")
    print()

    print("=== 6. Топ-5 товаров с наибольшим разбросом цен (max - min) ===")

    products_prices = defaultdict(list)
    for name, cat, price in products_data:
        products_prices[(name, cat)].append(price)

    price_spans = []
    for (name, cat), prices_list in products_prices.items():
        min_price = min(prices_list)
        max_price = max(prices_list)
        span = max_price - min_price
        price_spans.append((name, cat, min_price, max_price, span))

    price_spans.sort(key=lambda x: x[4], reverse=True)
    top_5 = price_spans[:5]

    print(f"{'Товар':<25} {'Категория':<15} {'Мин. цена':<12} {'Макс. цена':<12} {'Разброс':<12}")
    print("-" * 80)
    for name, cat, min_p, max_p, span in top_5:
        print(f"{name:<25} {cat:<15} {min_p:<12.2f} {max_p:<12.2f} {span:<12.2f}")

except psycopg2.OperationalError as e:
    print(f"Ошибка подключения к БД: {e}")
    print("Проверьте параметры подключения и запущен ли контейнер.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
    import traceback

    traceback.print_exc()
finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("\n✓ Соединение с базой данных закрыто.")
