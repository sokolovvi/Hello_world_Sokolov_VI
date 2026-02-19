
phenotype = input("Введите фенотип группы крови (I, II, III, IV): ").strip().upper()
if phenotype == "I":
    print("Группа крови: 0 (I)")
elif phenotype == "II":
    print("Группа крови: A (II)")
elif phenotype == "III":
    print("Группа крови: B (III)")
elif phenotype == "IV":
    print("Группа крови: AB (IV)")
else:
    print("Такой группы крови не существует")

type = input("Введите, Вы пациент или донор: ").strip().lower()
if type == "донор" and phenotype == "I":
    print("Вы можете отдавать кровь группам I, II, III, IV")
if type == "донор" and phenotype == "II":
    print("Вы можете отдавать кровь группам II, IV")
if type == "донор" and phenotype == "III":
    print("Вы можете отдавать кровь группам III, IV")
if type == "донор" and phenotype == "IV":
    print("Вы можете отдавать кровь только группе IV")
if type == "пациент" and phenotype == "I":
    print("Вы можете принимать кровь только у группы I")
if type == "пациент" and phenotype == "II":
    print("Вы можете принимать кровь у групп I, II")
if type == "пациент" and phenotype == "III":
    print("Вы можете принимать кровь у групп I, III")
if type == "пациент" and phenotype == "IV":
    print("Вы можете принимать кровь у групп I, II, III, IV")