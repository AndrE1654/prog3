import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt


# ручний ввід коду валюти
VALCODE = input("Введіть код валюти (наприклад JPY, USD, EUR): ").strip().lower()

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
    "&order=asc"
    "&json"
)

if response_data.status_code != 200:
    print("Помилка запиту:", response_data.status_code)
    exit()

data = response_data.json()

# ===== таблиця =====
print(f"\nКурс валюти {VALCODE.upper()} за попередній тиждень\n")
print(f"{'Дата':<15}{'Код':<6}{'Курс'}")
print(f"{'-'*15}{'-'*6}{'-'*10}")

dates = []
rates = []

for item in data:
    print(f"{item['exchangedate']:<15}{item['cc']:<6}{item['rate']}")
    dates.append(item["exchangedate"])
    rates.append(item["rate"])

# ===== графік =====
plt.figure()
plt.plot(dates, rates, marker="o")
plt.title(f"Зміна курсу валюти {VALCODE.upper()} за попередній тиждень")
plt.xlabel("Дата")
plt.ylabel("Курс (грн)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

