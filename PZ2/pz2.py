import hashlib


# базовий клас Користувач
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def __str__(self):
        return f"{self.__class__.__name__}(username='{self.username}', is_active={self.is_active})"


# підкласи Адміністратор,Звичайний користувач,Гість
class Administrator(User):
    def __init__(self, username, password, permissions):
        super().__init__(username, password)
        self.permissions = permissions


class RegularUser(User):
    def __init__(self, username, password, last_login=None):
        super().__init__(username, password)
        self.last_login = last_login


class GuestUser(User):
    def __init__(self, username):
        super().__init__(username, password="guest")


# клас Контроль доступу
class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)

        if not user:
            return None

        if not user.is_active:
            return None

        if isinstance(user, GuestUser):
            return user

        if user.verify_password(password):
            return user

        return None


# перевірка
if __name__ == "__main__":
    access_control = AccessControl()

    print("=== Створення користувачів ===")

    # Адміністратор
    admin_username = input("Введіть логін адміністратора: ")
    admin_password = input("Введіть пароль адміністратора: ")
    admin_permissions = input("Введіть дозволи (через кому): ").split(",")

    admin = Administrator(admin_username, admin_password, admin_permissions)
    access_control.add_user(admin)

    # Звичайний користувач
    user_username = input("\nВведіть логін користувача: ")
    user_password = input("Введіть пароль користувача: ")

    user = RegularUser(user_username, user_password)
    access_control.add_user(user)

    # Гість
    guest_username = input("\nВведіть логін гостя: ")
    guest = GuestUser(guest_username)
    access_control.add_user(guest)

    print("\n=== АВТЕНТИФІКАЦІЯ ===")
    login = input("Введіть логін: ")
    password = input("Введіть пароль (для гостя можна Enter): ")

    result = access_control.authenticate_user(login, password)

    if result:
        print("Успішний вхід:", result)
    else:
        print("Помилка входу")