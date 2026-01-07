import hashlib


def generate_file_hashes(*file_paths):
    """
    Приймає список шляхів до файлів (через *args).
    Для кожного файлу:
      - відкриває у бінарному режимі
      - рахує SHA-256
      - повертає словник: {path: sha256_hex}
    Обробляє FileNotFoundError та IOError.
    """
    result = {}

    for path in file_paths:
        try:
            sha256 = hashlib.sha256()

            with open(path, "rb") as f:
                # читаємо частинами (зручно для великих файлів)
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)

            result[path] = sha256.hexdigest()

        except FileNotFoundError:
            print(f"Помилка: файл '{path}' не знайдено.")
        except OSError as e:
            # OSError покриває IOError у сучасному Python
            print(f"Помилка читання файлу '{path}': {e}")

    return result


if __name__ == "__main__":
    # приклад запуску (вкажи свої файли, що реально є у папці)
    hashes = generate_file_hashes(
        "apache_logs.txt",
        "Task1.py",
        "Task2.py"
    )

    print("SHA-256 хеші файлів:")
    for file_path, file_hash in hashes.items():
        print(f"{file_path}: {file_hash}")
