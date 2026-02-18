total_capsules = int(input('Введите общее количество произведенных капсул: '))
capsules_in_package = int(input('Введите количество капсул в одной упаковке: '))

full_packages = total_capsules // capsules_in_package
remaining_capsules =  total_capsules % capsules_in_package
print('\n--- Отчет фасовочного цеха ---\n')
print(f'Полных упаковок:\t{full_packages}')
print(f'Остаток капсул:\t\t{remaining_capsules}')