import io
import base64
import matplotlib
matplotlib.use('Agg')  # для работы без графического интерфейса
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, jsonify, request, send_file
from sqlalchemy import create_engine

app = Flask(__name__)

# Параметры подключения к вашей БД (замените на свои)
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'student_task'

# Строка подключения для SQLAlchemy
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

def get_data(query):
    """Выполняет SQL-запрос и возвращает DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# ------------------------------------------------------------
# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------------------------------------
# API: статистические метрики (числовые)
@app.route('/api/stat/<metric>')
def get_stat(metric):
    """Возвращает JSON с вычисленной статистикой."""
    try:
        # Пример: таблица "grades", столбец "score"
        df = get_data("SELECT score FROM grades;")
        if df.empty:
            return jsonify({'error': 'Нет данных'}), 404
        
        scores = df['score']
        if metric == 'mean':
            value = scores.mean()
        elif metric == 'median':
            value = scores.median()
        elif metric == 'total':
            value = len(scores)
        elif metric == 'min':
            value = scores.min()
        elif metric == 'max':
            value = scores.max()
        elif metric == 'std':
            value = scores.std()
        else:
            return jsonify({'error': 'Неизвестная метрика'}), 400
        
        # Если значение – float, округляем до 2 знаков
        if isinstance(value, float):
            value = round(value, 2)
        
        return jsonify({'value': value, 'metric': metric})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------------------------------------------
# API: графики (возвращают PNG в формате base64)
@app.route('/api/chart/<kind>')
def get_chart(kind):
    try:
        # Загружаем данные
        df = get_data("SELECT score, course_id FROM grades;")  # подставьте свои столбцы
        if df.empty:
            return jsonify({'error': 'Нет данных'}), 404
        
        # Создаём график
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if kind == 'histogram':
            # Гистограмма распределения оценок
            ax.hist(df['score'], bins=10, color='skyblue', edgecolor='black')
            ax.set_title('Распределение оценок')
            ax.set_xlabel('Оценка')
            ax.set_ylabel('Частота')
            
            # Добавляем среднее и медиану на график
            mean_val = df['score'].mean()
            median_val = df['score'].median()
            ax.axvline(mean_val, color='red', linestyle='--', label=f'Среднее = {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', label=f'Медиана = {median_val:.2f}')
            ax.legend()
            
        elif kind == 'courses':
            # Столбчатая диаграмма: средний балл по курсам
            course_avg = df.groupby('course_id')['score'].mean().sort_values()
            course_avg.plot(kind='bar', ax=ax, color='orange', edgecolor='black')
            ax.set_title('Средний балл по курсам')
            ax.set_xlabel('Курс')
            ax.set_ylabel('Средняя оценка')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Дополнительно общая медиана (горизонтальная линия)
            overall_median = df['score'].median()
            ax.axhline(overall_median, color='blue', linestyle='--', label=f'Общая медиана = {overall_median:.2f}')
            ax.legend()
        else:
            return jsonify({'error': 'Неизвестный тип графика'}), 400
        
        # Сохраняем график в буфер в формате PNG
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        
        # Кодируем в base64 для передачи в JSON
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return jsonify({'image': img_base64, 'kind': kind})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)