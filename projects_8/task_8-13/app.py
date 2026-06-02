import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify, send_file
from sqlalchemy import create_engine

app = Flask(__name__)

# Параметры подключения к вашей БД
DB_USER = 'postgres_user'
DB_PASSWORD = 'postgres_password'
DB_HOST = 'localhost'
DB_PORT = '5430'
DB_NAME = 'postgres_db'

# Строка подключения для SQLAlchemy
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)


def get_data(query):
    """Выполняет SQL-запрос и возвращает DataFrame."""
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return pd.DataFrame()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/value/<metric>')
def get_stat(metric):
    """Возвращает JSON с вычисленной статистикой по ценам."""
    try:
        query = """
            SELECT pr.price
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
            WHERE pr.price IS NOT NULL;
        """
        df = get_data(query)

        if df.empty:
            return jsonify({'error': 'Нет данных о ценах'}), 404

        prices = df['price'].dropna()

        if len(prices) == 0:
            return jsonify({'error': 'Нет числовых данных'}), 404

        # Вычисляем метрику
        if metric == 'mean':
            value = prices.mean()
            label = "Средняя цена"
        elif metric == 'median':
            value = prices.median()
            label = "Медианная цена"
        elif metric == 'total':
            value = len(prices)
            label = "Количество записей"
        elif metric == 'sum':
            value = prices.sum()
            label = "Сумма цен"
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

        # Если значение – float, округляем до 2 знаков
        if isinstance(value, float):
            value = round(value, 2)

        return jsonify({
            'value': value,
            'metric': label
        })
    except Exception as e:
        print(f"Ошибка в get_stat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chart/<kind>')
def get_chart(kind):
    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        if kind == 'histogram':
            # Гистограмма распределения цен
            query = """
                SELECT pr.price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
                WHERE pr.price IS NOT NULL;
            """
            df = get_data(query)
            prices = df['price'].dropna()

            ax.hist(prices, bins=15, color='#2A9D8F', edgecolor='black', alpha=0.7)
            ax.set_title('Распределение цен на товары', fontsize=14, fontweight='bold')
            ax.set_xlabel('Цена (руб.)', fontsize=12)
            ax.set_ylabel('Частота', fontsize=12)
            ax.grid(True, alpha=0.3)

            # Добавляем статистику
            mean_val = prices.mean()
            median_val = prices.median()
            std_val = prices.std()

            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2,
                       label=f'Средняя = {mean_val:.2f} руб.')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2,
                       label=f'Медиана = {median_val:.2f} руб.')

            stats_text = f'Среднее: {mean_val:.2f}\nМедиана: {median_val:.2f}\nСт.отклонение: {std_val:.2f}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.legend()

        elif kind == 'categories':
            # Средняя цена по категориям
            query = """
                SELECT p.category, AVG(pr.price) as avg_price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
                WHERE pr.price IS NOT NULL
                GROUP BY p.category
                ORDER BY avg_price DESC;
            """
            df = get_data(query)

            if df.empty:
                return jsonify({'error': 'Нет данных по категориям'}), 404

            # Создаём столбчатую диаграмму
            bars = ax.bar(range(len(df)), df['avg_price'], color='#2A9D8F', edgecolor='black', alpha=0.7)
            ax.set_xticks(range(len(df)))
            ax.set_xticklabels(df['category'], rotation=45, ha='right')
            ax.set_title('Средняя цена по категориям', fontsize=14, fontweight='bold')
            ax.set_ylabel('Средняя цена (руб.)', fontsize=12)
            ax.set_xlabel('Категория', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')

            # Добавляем общую медиану
            query_all = "SELECT price FROM prices WHERE price IS NOT NULL;"
            df_all = get_data(query_all)
            overall_median = df_all['price'].median()
            ax.axhline(overall_median, color='red', linestyle='--', linewidth=2,
                       label=f'Общая медиана = {overall_median:.2f} руб.')

            # Добавляем значения на столбцы
            for i, (bar, val) in enumerate(zip(bars, df['avg_price'])):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                        f'{val:.2f}', ha='center', va='bottom', fontsize=9)

            ax.legend()

        elif kind == 'boxplot':
            # Боксплот распределения цен по категориям
            query = """
                SELECT p.category, pr.price
                FROM products p
                JOIN prices pr ON p.id = pr.product_id
                WHERE pr.price IS NOT NULL
                ORDER BY p.category;
            """
            df = get_data(query)

            if df.empty:
                return jsonify({'error': 'Нет данных'}), 404

            # Подготовка данных для boxplot по категориям
            categories = df['category'].unique()
            data_to_plot = []
            category_names = []
            for category in categories:
                category_data = df[df['category'] == category]['price'].values
                if len(category_data) > 0:
                    data_to_plot.append(category_data)
                    category_names.append(category)

            bp = ax.boxplot(data_to_plot, labels=category_names, patch_artist=True)
            for box in bp['boxes']:
                box.set_facecolor('#2A9D8F')
                box.set_alpha(0.7)

            ax.set_title('Распределение цен по категориям', fontsize=14, fontweight='bold')
            ax.set_ylabel('Цена (руб.)', fontsize=12)
            ax.set_xlabel('Категория', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')

        else:
            return jsonify({'error': 'Неизвестный тип графика'}), 400

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return send_file(buf, mimetype='image/png')

    except Exception as e:
        print(f"Ошибка в get_chart: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)