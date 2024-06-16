# user_interface.py
from database import session
from models import User, Item

def user_list():
    print("\nСписок всех пользователей:")
    users = session.query(User).all()
    if users:
        for user in users:
            print(f"Никнейм: {user.nickname}, Уровень профиля: {user.profile_level}, Количество продаж: {user.sales_count}, Баланс: {user.balance}")
    else:
        print("Нет зарегистрированных пользователей.")

def register():
    print("Регистрация нового пользователя")
    nickname = input("Введите никнейм: ")
    password = input("Введите пароль: ")

    existing_user = session.query(User).filter_by(nickname=nickname).first()
    if existing_user:
        print("Пользователь с таким никнеймом уже существует. Попробуйте другой никнейм.")
        return

    new_user = User(nickname=nickname, password=password)
    session.add(new_user)
    session.commit()
    print("Регистрация успешна! Теперь вы можете войти в систему.")

def login():
    print("Вход в систему")
    nickname = input("Введите никнейм: ")
    password = input("Введите пароль: ")

    user = session.query(User).filter_by(nickname=nickname, password=password).first()
    if user:
        print(f"Добро пожаловать, {user.nickname}!")
        user_main_menu(user)
    else:
        print("Неверный никнейм или пароль. Попробуйте снова.")

def user_main_menu(user):
    while True:
        print("\nМеню пользователя:")
        print("1. Вывод профиля")
        print("2. Просмотр торговой площадки")
        print("3. Выйти из системы")
        choice = input("Выберите опцию: ")

        if choice == "1":
            view_profile(user)
        elif choice == "2":
            view_marketplace(user)
        elif choice == "3":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def view_profile(user):
    while True:
        print("\nПрофиль пользователя:")
        print(f"Никнейм: {user.nickname}")
        print(f"Уровень профиля: {user.profile_level}")
        print(f"Количество продаж: {user.sales_count}")
        print(f"Текущий баланс: {user.balance}")

        # Выводим предметы пользователя
        if user.items:
            print("\nПредметы пользователя:")
            for item in user.items:
                print(f"Название: {item.name}, Описание: {item.description}, Тип: {item.item_type}, Цена: {item.price}")
        else:
            print("У вас нет предметов.")

        print("\nВыберите желаемое действие:")
        print("1. Пополнить баланс")
        print("2. Сменить никнейм")
        print("3. Добавить новый предмет на продажу")
        print("4. Изменить стоимость предмета")
        print("5. Выйти")
        choice = input("Выберите опцию: ")

        if choice == "1":
            add_balance(user)
        elif choice == "2":
            change_nickname(user)
        elif choice == "3":
            add_item(user)
        elif choice == "4":
            change_item_price(user)
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_balance(user):
    amount = float(input("Введите сумму для пополнения баланса: "))
    amount = amount if amount >= 0 else 0
    if amount == 0:
        print("Сумма должна быть положительной. Попробуйте снова.")
    else:
        user.balance += amount
        session.commit()
        print(f"Баланс успешно пополнен. Текущий баланс: {user.balance}")

def change_nickname(user):
    new_nickname = input("Введите новый никнейм: ")
    existing_user = session.query(User).filter_by(nickname=new_nickname).first()
    if existing_user:
        print("Пользователь с таким никнеймом уже существует. Попробуйте другой никнейм.")
    else:
        user.nickname = new_nickname
        session.commit()
        print("Никнейм успешно изменен.")

def add_item(user):
    name = input("Введите название предмета: ")
    description = input("Введите описание предмета: ")
    item_type = input("Введите тип предмета (Одежда, Курьеры, Варды, Ключи, Экраны, Руны, Интерфейсы, Игроки, Комментаторы): ")
    price = float(input("Введите цену предмета: "))

    new_item = Item(name=name, description=description, item_type=item_type, price=price, owner=user)
    session.add(new_item)
    session.commit()
    print("Предмет успешно добавлен на продажу.")

def change_item_price(user):
    item_name = input("Введите название предмета, стоимость которого хотите изменить: ")
    item = session.query(Item).filter_by(name=item_name, owner=user).first()
    if item:
        new_price = float(input("Введите новую стоимость предмета: "))
        item.price = new_price
        session.commit()
        print("Стоимость предмета успешно изменена.")
    else:
        print("Предмет не найден или вы не являетесь его владельцем.")

def view_marketplace(user):
    print("\nТорговая площадка:")
    categories = ["Одежда", "Курьеры", "Варды", "Ключи", "Экраны", "Руны", "Интерфейсы", "Игроки", "Комментаторы"]

    # Подсчитываем количество предметов в каждой категории, исключая предметы текущего пользователя
    category_counts = {}
    for category in categories:
        count = session.query(Item).filter(Item.item_type == category, Item.owner != user).count()
        category_counts[category] = count

    for category, count in category_counts.items():
        print(f"{category}: {count} предметов")

    while True:
        selected_category = input("\nВведите категорию для просмотра предметов (или 'выход' для возврата в меню): ")
        if selected_category.lower() == 'выход':
            break
        elif selected_category in categories:
            view_category_items(user, selected_category)
        else:
            print("Неверная категория. Попробуйте снова.")

def view_category_items(user, category):
    print(f"\nПредметы категории {category}:")
    items = session.query(Item).filter(Item.item_type == category, Item.owner != user).all()
    if items:
        for idx, item in enumerate(items):
            print(f"{idx + 1}. Название: {item.name}, Описание: {item.description}, Цена: {item.price}")
        
        while True:
            choice = input("\nВведите номер предмета для просмотра опций (или 'выход' для возврата к категориям): ")
            if choice.lower() == 'выход':
                break
            elif choice.isdigit() and int(choice):
                view_item_options(user, session.query(Item).get(int(choice)))
            else:
                print("Неверный выбор. Попробуйте снова.")
    else:
        print("В этой категории нет доступных предметов.")

def view_category_items(user, category):
    print(f"\nПредметы категории {category}:")
    items = session.query(Item).filter(Item.item_type == category, Item.owner != user).all()
    if items:
        for idx, item in enumerate(items):
            print(f"{idx + 1}. Название: {item.name}, Описание: {item.description}, Цена: {item.price}")
        
        while True:
            choice = input("\nВведите номер предмета для просмотра опций (или 'выход' для возврата к категориям): ")
            if choice.lower() == 'выход':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(items):
                view_item_options(user, items[int(choice) - 1])
            else:
                print("Неверный выбор. Попробуйте снова.")
    else:
        print("В этой категории нет доступных предметов.")

def view_item_options(user, item):
    while True:
        print(f"\nВыбранный предмет: {item.name}, Владелец: {item.owner.nickname}, Цена: {item.price}, ID: {item.id}")
        print("1. Купить предмет")
        print("2. Вернуться к категориям")
        choice = input("Выберите опцию: ")

        if choice == "1":
            buy_item(user, item)
        elif choice == "2":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def buy_item(user, item):
    print(f"\nПокупка предмета: {item.name}")
    owner_nickname = input("Введите никнейм владельца предмета: ")
    item_number = input("Введите номер предмета в инвентаре владельца: ")
    owner = session.query(User).filter_by(nickname=owner_nickname).first()
    if owner:
        items = session.query(Item).filter_by(owner=owner).all()
        if items and 0 < int(item_number) <= len(items) and items[int(item_number) - 1] == item:
            if user.balance >= item.price:
                user.balance -= item.price
                owner.balance += item.price
                item.owner = user
                session.commit()
                print(f"Предмет {item.name} успешно куплен!")
                return
            else:
                print("Недостаточно средств для покупки этого предмета.")
        else:
            print("Предмет не найден в инвентаре указанного пользователя.")
    else:
        print("Пользователь с указанным никнеймом не найден.")


def main_menu():
    while True:
        print("\nМеню:")
        print("1. Войти в систему")
        print("2. Зарегистрироваться")
        print("3. Вывод всех пользователей")
        print("4. Выйти из программы")
        choice = input("Выберите опцию: ")

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            user_list()
        elif choice == "4":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
