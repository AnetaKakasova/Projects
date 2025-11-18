import mysql.connector
from mysql.connector.connection import MySQLConnection, Error

# vytvoření připojení k databázi
def connection() ->MySQLConnection | None:
    try: 
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1111",
            database="task_manager"
            )
        return conn
    except Error as err:
        print("❌ Nepodařilo se připojit k databázi!")
        print(f"Chyba: {err}")
        return None


# tato funkce má za úkol vytvořit tabulku pro úkoly
def create_table(conn):
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                TaskID INT PRIMARY KEY AUTO_INCREMENT,
                Task_name VARCHAR(255) NOT NULL,
                Task_description TEXT NOT NULL,
                Task_state ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
                Creation_date DATE NOT NULL DEFAULT (CURRENT_DATE)
                );
            """)
    finally:
        cursor.close()
        conn.close()


# funkce pro zobrazení hlavního menu s výběrem ze 4 možností
def main_menu():
    print("Správce úkolů - hlavní menu\n1. Přidat nový úkol\n2. Zobrazit všechny úkoly\n3. Aktualizovat úkol \n4. Odstranit úkol\n5. Konec programu")
    function = input("Vyberte možnost (1-5): ")
    return function 


# tato funkce slouží pro vložení nového úkolu
def add_task(conn):
    cursor = conn.cursor(buffered=True)
    if not task_name or not task_description:
        print("❌ Chyba, název úkolu ani popisek nesmí být prázdný!")
    else:
        cursor.execute("INSERT INTO Tasks (Task_name, Task_description) VALUES (%s, %s);", (task_name, task_description))
        print("✅ Úkol byl úspěšně uložen do databáze.")
    conn.commit()
    cursor.close()
    conn.close()


# funkce pro zobrazení úkolů v databázi Tasks
def view_tasks(conn):
    cursor = conn.cursor(buffered=True)
    states = ("Nezahájeno", "Probíhá")
    cursor.execute("SELECT TaskID, Task_name, Task_description, Task_state from Tasks WHERE Task_state IN (%s,%s)", states)
    tasks = cursor.fetchall()
    if not tasks:
        print("Seznam úkolů je prázdný.")
    else:
        print("Seznam úkolů:")
        for task in tasks:
            print(f"{task[0]} - {task[1]} - {task[2]} - {task[3]}")
    cursor.close()
    conn.close()


def update_task(conn, choosen_task, choosen_state):
    tasks_list = []
    cursor = conn.cursor(buffered=True)
    states = ("Nezahájeno", "Probíhá")
    cursor.execute("SELECT * FROM Tasks WHERE Task_state IN (%s, %s);", states)
    for task in cursor.fetchall():
        tasks_list.append(f'{task[0]}')

    if choosen_task.isnumeric():
        if choosen_task not in tasks_list:
            print("❌ Byl vybrán neexistující úkol!")
        else:
            if choosen_state == "1":
                cursor.execute("UPDATE tasks SET Task_state = %s WHERE TaskID = %s;", ("Probíhá", choosen_task))
                conn.commit()
                print("✅ Stav úkolu byl úspěšně změněn na: Probíhá")
            elif choosen_state == "2":
                cursor.execute("UPDATE tasks SET Task_state = %s WHERE TaskID = %s;", ("Hotovo", choosen_task))
                conn.commit()
                print("✅ Stav úkolu byl úspěšně změněn na: Hotovo")
            else:
                print("❌ Byla vybrána neplatná možnost!")
    else: 
        print("❌ Byl zadán neplatný vstup!")

    cursor.close()
    conn.close()


# tato funkce je pro smazání úkolu
def delete_task(conn, choosen_task):
    tasks_list = []
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Tasks")
    for task in cursor.fetchall():
        tasks_list.append(f'{task[0]}')

    if choosen_task not in tasks_list:
        print("❌ Byl vybrán neexistující úkol!")
    else: 
        cursor.execute("DELETE FROM Tasks WHERE TaskID = %s;", (choosen_task,))
        conn.commit()
        print("✅ Úkol byl úspěšně smazán.")
    cursor.close()
    conn.close()


while True:

    conn = connection()
    create_table(conn)
    function_selection = main_menu()
    

    if function_selection == "1":
        conn = connection()
        task_name = input("Zadejte název úkolu: ")
        task_description = input("Zadejte popis úkolu: ")
        add_task(conn)
    elif function_selection == "2":
        conn = connection()
        view_tasks(conn)
    elif function_selection == "3":
        conn = connection()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM Tasks;")
        for task in cursor.fetchall():
            print(f"{task[0]} - {task[1]} - {task[2]} - {task[3]} - {task[4]}")
        choosen_task = input("Zadejte ID úkolu, který chcete aktualizovat: ")
        choosen_state = input("Vyberte stav, který chcete úkolu přiřadit:\n1. Probíhá\n2. Hotovo\nVybraný stav: ")
        update_task(conn, choosen_task, choosen_state)
    elif function_selection == "4":
        conn = connection()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM Tasks;")
        for task in cursor.fetchall():
            print(f"{task[0]} - {task[1]} - {task[2]} - {task[3]} - {task[4]}")
        choosen_task = input("Zadejte ID úkolu, který chcete smazat: ")
        delete_task(conn, choosen_task)
    elif function_selection == "5":
        exit("Konec programu.")
    else:
        print("Byla vybrána neplatná funkce. Zadejte prosím platnou možnost: ")
        continue