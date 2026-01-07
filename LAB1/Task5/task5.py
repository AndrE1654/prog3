import hashlib

# "База" користувачів: login -> {password_hash, full_name}
users = {
    "andr3": {
        "password_hash": hashlib.md5("NADIYA".encode("utf-8")).hexdigest(),
        "full_name": "Качанов Андрій Артурович"
    },
    "REZ": {
        "password_hash": hashlib.md5("MILANA".encode("utf-8")).hexdigest(),
        "full_name": "Резник Ілля Андрійович"
    },
    "tajikistan": {
        "password_hash": hashlib.md5("Opel1.8".encode("utf-8")).hexdigest(),
        "full_name": "Аслонов Амир Шоханшоїович"
    }
}

def md5_hash(password: str) -> str:
    """Повертає md5-хеш пароля у вигляді hex-рядка."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def check_user_password(login: str, users_db: dict) -> bool:
    """
     пароль через input() і перевіряє його для вказаного login.
    Перевірка True or False.
    """
    if login not in users_db:
        print("Користувача з таким login не знайдено.")
        return False

    entered_password = input("Введіть пароль: ")
    entered_hash = md5_hash(entered_password)

    if entered_hash == users_db[login]["password_hash"]:
        print(f"Успішний вхід. Вітаємо, {users_db[login]['full_name']}!")
        return True
    else:
        print("Невірний пароль.")
        return False

if __name__ == "__main__":
    login = input("Введіть login: ")
    check_user_password(login, users)
