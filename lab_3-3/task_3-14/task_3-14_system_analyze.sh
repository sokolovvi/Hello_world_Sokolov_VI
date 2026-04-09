#!/bin/bash

echo "========================================="
echo "         АНАЛИЗ ДИСКОВОГО ПРОСТРАНСТВА"
echo "========================================="
echo ""


df -h | awk '
NR > 1 {
    filesystem = $1
    use_percent = $5
    
    
    gsub(/%/, "", use_percent)
    
    
    printf "   %-20s %3s%%\n", filesystem, $5
    
    
    if (use_percent > 90) {
        print "   ⚠️  ПРЕДУПРЕЖДЕНИЕ: Файловая система " filesystem " заполнена на " $5 "!"
    }
}
'

echo ""
echo "========================================="
