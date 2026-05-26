const resultArea = document.getElementById('result-area');
const buttons = document.querySelectorAll('.action-btn:not(.clear)');
const clearBtn = document.getElementById('clear-btn');

// Функция отображения состояния загрузки
function showLoading() {
    resultArea.innerHTML = '<div class="loading">⏳ Загрузка...</div>';
}

// Функция отображения ошибки
function showError(message) {
    resultArea.innerHTML = `<div class="error">❌ Ошибка: ${message}</div>`;
}

// Функция отображения числовой статистики
function showStat(value, metricName) {
    const metricNames = {
        mean: 'Средний балл',
        median: 'Медиана',
        total: 'Количество оценок',
        min: 'Минимальная оценка',
        max: 'Максимальная оценка'
    };
    const label = metricNames[metricName] || metricName;
    resultArea.innerHTML = `
        <div class="stat-card">
            <div class="label">${label}</div>
            <div class="value">${value}</div>
        </div>
    `;
}

// Функция отображения графика (base64)
function showChart(base64Image, kind) {
    resultArea.innerHTML = `
        <div class="chart-container">
            <img src="data:image/png;base64,${base64Image}" alt="График">
        </div>
    `;
}

// Обработчик клика по кнопкам
buttons.forEach(btn => {
    btn.addEventListener('click', async () => {
        const action = btn.dataset.action;
        if (action === 'stat') {
            const metric = btn.dataset.metric;
            showLoading();
            try {
                const response = await fetch(`/api/stat/${metric}`);
                const data = await response.json();
                if (response.ok) {
                    showStat(data.value, metric);
                } else {
                    showError(data.error || 'Неизвестная ошибка');
                }
            } catch (err) {
                showError('Сетевая ошибка: ' + err.message);
            }
        } else if (action === 'chart') {
            const kind = btn.dataset.kind;
            showLoading();
            try {
                const response = await fetch(`/api/chart/${kind}`);
                const data = await response.json();
                if (response.ok) {
                    showChart(data.image, kind);
                } else {
                    showError(data.error || 'Ошибка при генерации графика');
                }
            } catch (err) {
                showError('Сетевая ошибка: ' + err.message);
            }
        }
    });
});

// Кнопка очистки
clearBtn.addEventListener('click', () => {
    resultArea.innerHTML = '<p class="placeholder">← Нажмите кнопку, чтобы увидеть результат</p>';
});