tasks = list()

def main_menu():
    print("Správce úkolů - hlavní menu\n1. Přidat nový úkol\n2. Zobrazit všechny úkoly\n3. Odstranit úkol\n4. Konec programu")
    function = input("Vyberte možnost (1-4): ")
    return function 


def add_task():
    while True:
        task_name = input("Zadejte název úkolu: ")
        task_description = input("Zadejte popis úkolu: ")

        if len(task_name) != 0 and len(task_description) != 0:
            task = {"name": task_name,"description": task_description}
            tasks.append(task)
            print(f"Úkol '{tasks[-1]["name"]} - {tasks[-1]["description"]}' byl přidán.")
            break
        else:
            print("Zadali jste prázdný vstup. Zadejte prosím znovu název úkolu i popis úkolu.")
            continue
   
    
def view_tasks():
    if len(tasks) != 0:
        print("Seznam úkolů:")
        for line, _ in enumerate(tasks, start=1):
            print(f"{line}. {tasks[line-1]["name"]} - {tasks[line-1]["description"]}")
    else:
        print("Seznam úkolů je prázdný.")


def delete_task():
    view_tasks()
    if len(tasks) != 0:
        while True:
            task_deletion = input("Zadejte číslo úkolu, který chcete odstranit: ")
            try:
                task_deletion = int(task_deletion)
                break
            except ValueError: 
                print("Zadali jste neplatný vstup. Prosím zadejte existující číslo úkolu.")
                continue

        if task_deletion > 0 and task_deletion <= len(tasks):
            print(f"Úkol '{tasks[task_deletion-1]["name"]} - {tasks[task_deletion-1]["description"]}' byl odstraněn.")
            del tasks[task_deletion-1]
        else:
            print("Zadali jste neexistující číslo úkolu. Prosím zadejte číslo úkolu, který existuje.")
            delete_task()
    else:
        print("Není k dispozici žádný úkol ke smazání.")



while True:
    function_selection = main_menu()

    if function_selection == "1":
        add_task()
    elif function_selection == "2":
        view_tasks()
    elif function_selection == "3":
        delete_task()
    elif function_selection == "4":
        exit("Konec programu.")
    else:
        print("Byla vybrána neplatná funkce. Zadejte prosím platnou možnost: ")
        continue