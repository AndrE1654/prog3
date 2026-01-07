import re

def analyze_log_file(log_file_path):
    status_counts = {}

    # HTTP-код — три цифри після лапок
    status_pattern = re.compile(r'"\s(\d{3})\s')

    try:
        with open(log_file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                match = status_pattern.search(line)
                if match:
                    code = match.group(1)
                    status_counts[code] = status_counts.get(code, 0) + 1

    except FileNotFoundError:
        print(f"Помилка: файл '{log_file_path}' не знайдено.")
    except IOError as e:
        print(f"Помилка читання файлу '{log_file_path}': {e}")

    return status_counts


if __name__ == "__main__":
    result = analyze_log_file("apache_logs.txt")
    print(result)
