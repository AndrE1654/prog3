tasks = {}

def add_task(name, status="очікує"):
    tasks[name] = status

def delete_task(name):
    if name in tasks:
        del tasks[name]

def change_status(name, status):
    if name in tasks:
        tasks[name] = status

def waiting_tasks():
    return [task for task, status in tasks.items() if status == "очікує"]
# приклад використання
add_task("лаба", "в процесі")
add_task("звіт")
add_task("захист", "виконано")

change_status("звіт", "в процесі")
delete_task("захист")

print(tasks)
print("Очікує:", waiting_tasks())
