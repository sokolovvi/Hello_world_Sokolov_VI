#!/bin/bash

echo "========================================="
echo "   ПОДСЧЕТ НУКЛЕОТИДОВ В FASTA-ФАЙЛАХ"
echo "========================================="
echo ""


if [ -z "$(ls *.fasta 2>/dev/null)" ]; then
    echo "❌ Ошибка: В текущей директории нет файлов *.fasta"
    echo "   Создайте хотя бы один FASTA-файл для анализа."
    exit 1
fi


printf "%-20s %-8s %-8s %-8s %-8s\n" "Файл" "A" "T" "G" "C"
printf "%-20s %-8s %-8s %-8s %-8s\n" "--------------------" "--------" "--------" "--------" "--------"


for file in *.fasta; do
    
    if [ ! -s "$file" ]; then
        echo "⚠️  Пропуск пустого файла: $file"
        continue
    fi
    
    
    SEQUENCE=$(grep -v "^>" "$file" | tr -d '\n' | tr -d '\r' | tr '[:lower:]' '[:upper:]')
    
    
    A_COUNT=$(echo "$SEQUENCE" | grep -o "A" | wc -l)
    T_COUNT=$(echo "$SEQUENCE" | grep -o "T" | wc -l)
    G_COUNT=$(echo "$SEQUENCE" | grep -o "G" | wc -l)
    C_COUNT=$(echo "$SEQUENCE" | grep -o "C" | wc -l)
    
    
    printf "%-20s %-8d %-8d %-8d %-8d\n" "$file" "$A_COUNT" "$T_COUNT" "$G_COUNT" "$C_COUNT"
done

echo ""
echo "========================================="
echo "           АНАЛИЗ ЗАВЕРШЕН"
echo "========================================="
