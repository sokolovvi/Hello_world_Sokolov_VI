
#!/bin/bash

FILE_PATH="./system.log"
ERROR_CODE=1

echo "========================================="
echo "         АНАЛИЗ ЛОГ-ФАЙЛА"
echo "========================================="


if [ -f "$FILE_PATH" ]; then
    echo "✅ Лог-файл найден: $FILE_PATH"
 
 
    FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null)
    echo "   Размер файла: $FILE_SIZE байт"
else
    echo "❌ Ошибка: файл $FILE_PATH не существует."
fi

echo ""


echo "Анализ кода ошибки:"

case $ERROR_CODE in
    0)
        echo "✅ Статус: Ошибок нет." ;;
    1)
        echo "❌ Статус: Критическая ошибка!" ;;
    2)
        echo "⚠️  Статус: Предупреждение (некритичная ошибка)." ;;
    3)
        echo "⚠️  Статус: Ошибка ввода/вывода." ;;
    *)
        echo "❓ Статус: Неизвестный код ($ERROR_CODE)." ;;
esac

echo "========================================="
