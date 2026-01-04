# список продажів
sales = [
    {"продукт": "пломбір 19% (циліндр)", "кількість": 4, "ціна": 320},
    {"продукт": "пломбір 19% (на паличці)", "кількість": 28, "ціна": 45},
    {"продукт": "пломбір 12% (вафельний стаканчик)", "кількість": 30, "ціна": 40},
]


def calculate_total_income(sales_list):
    """
    Обчислює загальний дохід для кожного продукту.
    Повертає словник: {назва продукту: загальний дохід}
    """
    income = {}

    for sale in sales_list:
        name = sale["продукт"]
        total = sale["кількість"] * sale["ціна"]

        if name in income:
            income[name] += total
        else:
            income[name] = total

    return income


# підрахунок доходу
income_per_product = calculate_total_income(sales)

# продукти з доходом > 1000
income_over_1000 = []
for product, total in income_per_product.items():
    if total > 1000:
        income_over_1000.append(product)

print("Загальний дохід по продуктах:", income_per_product)
print("Продукти з доходом більше 1000:", income_over_1000)
