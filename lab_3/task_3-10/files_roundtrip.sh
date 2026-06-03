#!/bin/bash

echo "========================================="
echo "   FILES ROUNDTRIP: Создание и удаление"
echo "========================================="
echo ""


echo "📁 [ЦИКЛ FOR] Создание файлов test1.txt ... test10.txt:"

for i in {1..10}; do
    FILENAME="test$i.txt"
    touch "$FILENAME"
    echo "   ✅ Создан: $FILENAME"
done


echo ""
echo "📋 Содержимое директории после создания:"
ls -la test*.txt 2>/dev/null | awk '{print "   " $9}'

echo ""
echo "========================================="
echo ""


echo "🗑️  [ЦИКЛ WHILE] Удаление файлов в обратном порядке:"

counter=10
while [ $counter -ge 1 ]; do
    FILENAME="test$counter.txt"
    
    if [ -f "$FILENAME" ]; then
        rm "$FILENAME"
        echo "   ✅ Удален: $FILENAME (осталось: $((counter-1)))"
    else
        echo "   ⚠️  Файл не найден: $FILENAME"
    fi
    
    ((counter--))
done

echo ""
echo "========================================="
echo ""


echo "🔍 Проверка: остались ли файлы test*.txt?"
remaining=$(ls test*.txt 2>/dev/null)
if [ -z "$remaining" ]; then
    echo "   ✅ Все файлы успешно удалены. Директория чиста."
else
    echo "   ⚠️  Остались файлы: $remaining"
fi

echo ""
echo "========================================="
echo "           РАБОТА ЗАВЕРШЕНА"
echo "========================================="
