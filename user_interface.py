# user_interface.py
from database import session
from models import User, Item

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
        print("\nОсновное меню:")
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
        print("3. Выйти из программы")
        choice = input("Выберите опцию: ")

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
