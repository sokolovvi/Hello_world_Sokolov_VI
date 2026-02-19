choice = input("Введите, куда Вы пойдёте(налево, направо или прямо): ").strip().lower()
if choice == "налево":
    print("Богатым будешь")
elif choice == "направо":
    print("женатым будешь")
elif choice == "прямо":
    print("убитым будешь")
else:
    print('Введите корректно !!!')
