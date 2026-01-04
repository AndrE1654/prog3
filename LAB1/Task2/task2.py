warehouse = {
    "пломбір 19% (циліндр) 1кг": 6,
    "пломбір 19% (на паличці) 75г": 3,
    "пломбір 12% (вафельний стаканчик) 70г": 10
}

def change_amount(product_name, qty):
   
    if product_name in warehouse:
        warehouse[product_name] = warehouse[product_name] + qty
    else:
        
        if qty > 0:
            warehouse[product_name] = qty

    
    if product_name in warehouse and warehouse[product_name] <= 0:
        del warehouse[product_name]


# приклади змін
change_amount("пломбір 19% (на паличці) 75г", 4)   # додали
change_amount("пломбір 12% (вафельний стаканчик) 70г", -7)  # забрали
change_amount("пломбір 19% (циліндр) 1кг", -10)    # забрали більше ніж було -> видалиться

low_stock = []
for name, amount in warehouse.items():
    if amount < 5:
        low_stock.append(name)

print("склад:", warehouse)
print("менше ніж 5:", low_stock)
