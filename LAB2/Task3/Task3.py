import re
from collections import Counter


def filter_ips(input_file_path, output_file_path, allowed_ips):
    """
    Аналізує IP-адреси з лог-файлу http-сервера.
    - читає IP з кожного рядка input_file_path
    - бере лише ті IP, які є в allowed_ips
    - рахує кількість входжень дозволених IP
    - записує у output_file_path у форматі: "<ip> - <кількість>"
    - обробляє FileNotFoundError та IOError
    """

    # шаблон для IP на початку рядка (типовий apache log)
    ip_pattern = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3})")

    counts = Counter()

    try:
        # 1) читаємо вхідний файл
        with open(input_file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = ip_pattern.search(line)
                if not match:
                    continue

                ip = match.group(1)

                # 2) перевіряємо чи IP дозволений
                if ip in allowed_ips:
                    # 3) рахуємо входження
                    counts[ip] += 1

        # 4) записуємо у вихідний файл
        try:
            with open(output_file_path, "w", encoding="utf-8") as out:
                for ip, c in counts.items():
                    out.write(f"{ip} - {c}\n")

        except IOError as e:
            print(f"Помилка запису у файл '{output_file_path}': {e}")
            return {}

    except FileNotFoundError:
        print(f"Помилка: файл '{input_file_path}' не знайдено.")
        return {}

    except IOError as e:
        print(f"Помилка читання файлу '{input_file_path}': {e}")
        return {}

    return dict(counts)


if __name__ == "__main__":
    # приклад списку дозволених IP (зроби свої/з логів)
    allowed_ips = [
        "83.149.9.216",
        "66.249.73.135",
        "168.41.191.40",
        "46.105.14.53",
    ]

    result = filter_ips(
        input_file_path="apache_logs.txt",
        output_file_path="allowed_ips_report.txt",
        allowed_ips=allowed_ips
    )

    print("Результат (словник):")
    print(result)
    print("Файл 'allowed_ips_report.txt' створено.")
