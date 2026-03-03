files = ["seq1", "seq2", "seq3", "seq4"]

for name in files:

   new_name = name + ".fasta"

   print(f"{new_name}")

from datetime import date
d = date(2026, 2, 22)

print(f"Объект date: {d}")
print(f"Год: {d.year}")
print(f"Месяц: {d.month}")
print(f"День: {d.day}")