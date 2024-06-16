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
            view_marketplace()
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

def view_marketplace():
    print("\nТорговая площадка:")
    items = session.query(Item).all()
    if items:
        for item in items:
            print(f"Название: {item.name}, Описание: {item.description}, Тип: {item.item_type}, Цена: {item.price}")
    else:
        print("Торговая площадка пуста.")

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
