#!/bin/bash


readonly CURRENT_YEAR=2026
BIRTH_YEAR=2000


AGE=$((CURRENT_YEAR - BIRTH_YEAR))


echo "Текущий год: $CURRENT_YEAR"
echo "Год рождения: $BIRTH_YEAR"
echo "Ваш примерный возраст: $AGE лет"
