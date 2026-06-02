import io
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, jsonify, send_file
from sqlalchemy import create_engine

app = Flask(__name__)

# Параметры подключения
DATABASE_URL = 'postgresql://postgres_user:postgres_password@localhost:5430/postgres_db'
engine = create_engine(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


# Маршруты для статистики
@app.route('/api/value/<metric>')
def get_stat(metric):
    try:
        query = """
            SELECT pr.price
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
        """
        df = pd.read_sql(query, engine)
        prices = df['price']

        if metric == 'mean':
            value = prices.mean()
            label = "Средняя цена"
        elif metric == 'median':
            value = prices.median()
            label = "Медианная цена"
        elif metric == 'total':
            value = len(prices)
            label = "Количество записей"
        elif metric == 'min':
            value = prices.min()
            label = "Минимальная цена"
        elif metric == 'max':
            value = prices.max()
            label = "Максимальная цена"
        elif metric == 'std':
            value = prices.std()
            label = "Стандартное отклонение"
        else:
            return jsonify({'error': 'Неизвестная метрика'}), 400

        return jsonify({'value': round(float(value), 2), 'metric': label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Маршрут для гистограммы
@app.route('/api/chart/histogram')
def get_histogram():
    try:
        query = "SELECT pr.price FROM products p JOIN prices pr ON p.id = pr.product_id"
        df = pd.read_sql(query, engine)
        prices = df['price']

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(prices, bins=15, color='#2A9D8F', edgecolor='black', alpha=0.7)
        ax.set_title('Распределение цен', fontsize=14)
        ax.set_xlabel('Цена (руб.)')
        ax.set_ylabel('Частота')
        ax.axvline(prices.mean(), color='red', linestyle='--', label=f'Среднее: {prices.mean():.2f}')
        ax.axvline(prices.median(), color='green', linestyle='--', label=f'Медиана: {prices.median():.2f}')
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Маршрут для графика "Средняя цена по категориям"
@app.route('/api/chart/categories')
def get_categories_chart():
    try:
        query = """
            SELECT p.category, AVG(pr.price) as avg_price
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
            GROUP BY p.category
            ORDER BY avg_price DESC;
        """
        df = pd.read_sql(query, engine)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(df)), df['avg_price'], color='#2A9D8F', edgecolor='black')
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df['category'], rotation=45, ha='right')
        ax.set_title('Средняя цена по категориям', fontsize=14, fontweight='bold')
        ax.set_ylabel('Средняя цена (руб.)')
        ax.set_xlabel('Категория')
        ax.grid(True, alpha=0.3, axis='y')

        # Добавляем значения на столбцы
        for i, (bar, val) in enumerate(zip(bars, df['avg_price'])):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    f'{val:.0f}', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Маршрут для боксплота
@app.route('/api/chart/boxplot')
def get_boxplot():
    try:
        query = """
            SELECT p.category, pr.price
            FROM products p
            JOIN prices pr ON p.id = pr.product_id;
        """
        df = pd.read_sql(query, engine)

        fig, ax = plt.subplots(figsize=(10, 6))
        categories = df['category'].unique()
        data_to_plot = [df[df['category'] == cat]['price'].values for cat in categories]

        bp = ax.boxplot(data_to_plot, labels=categories, patch_artist=True)
        for box in bp['boxes']:
            box.set_facecolor('#2A9D8F')
            box.set_alpha(0.7)

        ax.set_title('Распределение цен по категориям', fontsize=14, fontweight='bold')
        ax.set_ylabel('Цена (руб.)')
        ax.set_xlabel('Категория')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)