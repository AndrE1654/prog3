import requests

# GET-запит до API НБУ (Запит курсу євро до гривні за останній тиждень 31.12.2025 – 06.01.2026)
response_data = requests.get(
    "https://bank.gov.ua/NBU_Exchange/exchange_site"
    "?start=20251231"
    "&end=20260106"
    "&valcode=eur"
    "&sort=exchangedate"
    "&order=desc"
    "&json"
)

# перевірка статусу відповіді
if response_data.status_code != 200:
    print("Помилка запиту:", response_data.status_code)
    exit()

# отримання JSON-даних
data = response_data.json()

# вивід результатів
print("Дата\t\tКод\tКурс")
print("-" * 30)

for item in data:
    exchangedate = item["exchangedate"]
    cc = item["cc"]
    rate = item["rate"]
    print(f"{exchangedate}\t{cc}\t{rate}")
