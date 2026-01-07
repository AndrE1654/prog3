import requests
from datetime import date, timedelta

# ручний ввід коду валюти
VALCODE = input("Введіть код валюти (наприклад JPY, EUR): ").strip().lower()

# перевірка: код валюти обов'язковий
if not VALCODE:
    print("Помилка: код валюти не введено.")
    exit()

# попередній тиждень
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=6)

start_str = start_date.strftime("%Y%m%d")
end_str = end_date.strftime("%Y%m%d")

# GET-запит до API НБУ
response_data = requests.get(
    "https://bank.gov.ua/NBU_Exchange/exchange_site"
    f"?start={start_str}"
    f"&end={end_str}"
    f"&valcode={VALCODE}"
    "&sort=exchangedate"
    "&order=desc"
    "&json"
)

# перевірка статусу
if response_data.status_code != 200:
    print("Помилка запиту:", response_data.status_code)
    exit()

# JSON-відповідь
data = response_data.json()

# вивід результатів
print(f"\nКурс валюти {VALCODE.upper()} за попередній тиждень")
print(f"{'Дата':<15}{'Код':<8}{'Курс'}")
print(f"{'-'*15}{'-'*8}{'-'*10}")


for item in data:
    print(f"{item['exchangedate']:<15}{item['cc']:<6}{item['rate']}")

