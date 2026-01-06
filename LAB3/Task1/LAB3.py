import hashlib
import sqlite3
from pathlib import Path

# База зберігається поруч із файлом .py
DB_PATH = Path(__file__).resolve().parent / "users.db"


def hash_password(password: str) -> str:
    """Повертає SHA-256 хеш пароля."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection() -> sqlite3.Connection:
    """Створює з'єднання з SQLite базою."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Створює таблицю users, якщо її ще немає."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL
            );
            """
        )


def add_user(login: str, password: str, full_name: str) -> bool:
    """Додає нового користувача. Повертає False, якщо логін вже існує."""
    password_h = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (login, password_hash, full_name) VALUES (?, ?, ?)",
                (login, password_h, full_name),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate(login: str, password: str) -> bool:
    """Перевіряє автентифікацію: чи збігається введений пароль з хешем у БД."""
    password_h = hash_password(password)

    with get_connection() as conn:
        cur = conn.execute(
            "SELECT password_hash FROM users WHERE login = ?",
            (login,),
        )
        row = cur.fetchone()

    return bool(row and row[0] == password_h)


def update_password(login: str, old_password: str, new_password: str) -> bool:
    """
    Оновлює пароль користувача ТІЛЬКИ якщо введено правильний старий пароль.
    True — якщо оновлено, False — якщо логіна нема або старий пароль невірний.
    """
    if not authenticate(login, old_password):
        return False

    new_h = hash_password(new_password)

    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE users SET password_hash = ? WHERE login = ?",
            (new_h, login),
        )
        return cur.rowcount > 0


def main() -> None:
    init_db()

    while True:
        print("\nоберіть дію:")
        print("1. додати нового користувача")
        print("2. оновити пароль користувача")
        print("3. перевірити автентифікацію")
        print("4. вийти")

        choice = input("ваш вибір: ").strip()

        if choice == "1":
            login = input("логін: ").strip()
            full_name = input("піб: ").strip()
            password = input("пароль: ")

            if add_user(login, password, full_name):
                print("користувача додано успішно.")
            else:
                print("користувач з таким логіном вже існує.")

        elif choice == "2":
            login = input("логін користувача: ").strip()
            old_password = input("старий пароль: ")
            new_password = input("новий пароль: ")

            if update_password(login, old_password, new_password):
                print("пароль оновлено.")
            else:
                print("не вдалося оновити пароль (логін або старий пароль невірні).")

        elif choice == "3":
            login = input("логін: ").strip()
            password = input("пароль: ")

            if authenticate(login, password):
                print("автентифікація успішна.")
            else:
                print("невірний логін або пароль.")

        elif choice == "4":
            print("завершення роботи.")
            break

        else:
            print("невірний вибір. спробуйте ще раз.")


if __name__ == "__main__":
    main()
