import mysql.connector
from mysql.connector.connection import MySQLConnection, Error

# vytvoření připojení k databázi + chybová hláška v případě, že připojení selže
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


# funkce pro vytvoření tabulky tasks v případě, že ještě neexistuje
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


# funkce pro přidání nového úkolu + ověření prázdného vstupu
def add_task(conn, task_name, task_description):
    cursor = conn.cursor(buffered=True)
    if not task_name or not task_description:
        print("❌ Chyba, název úkolu ani popisek nesmí být prázdný!")
    else:
        cursor.execute("INSERT INTO Tasks (Task_name, Task_description) VALUES (%s, %s);", (task_name, task_description))
        print("✅ Úkol byl úspěšně uložen do databáze.")
    conn.commit()
    cursor.close()
    conn.close()


# funkce pro zobrazení úkolů
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


# ˇfunkce pro aktualizaci stavu úkolu + ověření chybného výběru
def update_task(conn, choosen_task, choosen_state):
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Tasks")

    if choosen_task.isnumeric() is True:
        if choosen_state =="1":
            cursor.execute("UPDATE tasks SET Task_state = 'Probíhá' WHERE TaskID = %s;", (choosen_task,))
            conn.commit()
            print('\n✅ Status úkolu byl aktualizován.\n')
        elif choosen_state == "2":
            cursor.execute("UPDATE tasks SET Task_state = 'Hotovo' WHERE TaskID = %s;", (choosen_task,))
            conn.commit()
            print('\n✅ Status úkolu byl aktualizován.\n')
        else:
            print('\n❌ Chybná volba nového stavu.\n')
    else:
        print("❌ Chybná volba ID úkolu.\n")

    cursor.close()
    conn.close()

# tato funkce je pro smazání úkolu + ověření, že úkol existuje
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

# funkce pro zobrazení hlavního menu s výběrem ze 4 možností + volání vybrané funkce
def main_menu():
    while True:
        print("Správce úkolů - hlavní menu\n1. Přidat nový úkol\n2. Zobrazit všechny úkoly\n3. Aktualizovat úkol \n4. Odstranit úkol\n5. Konec programu")
        function_selection = input("Vyberte možnost (1-5): ")
    

        if function_selection == "1":
            conn = connection()
            task_name = input("Zadejte název úkolu: ")
            task_description = input("Zadejte popis úkolu: ")
            add_task(conn, task_name, task_description)
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


# Ověření, zda došlo k úspěšnému připojení. Podkud ano, spustí se funkce pro vytvoření tabulky a spuštění hlavního menu.
if __name__ == '__main__':
    conn = connection()
    if conn is not None:
        create_table(connection())
        main_menu()
    else:
        print("Připojení selhalo")