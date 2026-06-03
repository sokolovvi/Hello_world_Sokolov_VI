#!/bin/bash

echo "========================================="
echo "       ЧИСЛОВОЙ ФИЛЬТР (1-20)"
echo "========================================="
echo "Выводим нечетные числа до 15:"
echo ""


for i in {1..20}; do
    
    if [ $((i % 2)) -eq 0 ]; then
        continue
    fi
    
    
    if [ $i -eq 15 ]; then
        echo "   $i (остановка по break)"
        break
    fi
    
    
    echo "   $i"
done
