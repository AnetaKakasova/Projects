import mysql.connector
from mysql.connector.connection import MySQLConnection, Error
from dotenv import load_dotenv
import os


# vytvoření připojení k databázi + chybová hláška v případě, že připojení selže
def connection() ->MySQLConnection | None:
    try: 
        conn = mysql.connector.connect(
            host=os.getenv("DB_TM_HOST"),
            user=os.getenv("DB_TM_USER"),
            password=os.getenv("DB_TM_PASSWORD"),
            # database=os.getenv("DB_TM_NAME")
            )
        return conn
    except Error as err:
        print("❌ Nepodařilo se připojit k databázi!\n")
        print(f"Chyba: {err}")
        return None

# funkce pro vytvoření databáze a tabulky
def create_table(conn):
    cursor = conn.cursor(buffered=True)
    cursor.execute("CREATE DATABASE IF NOT EXISTS Task_manager")
    conn.database = "Task_manager"

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INT PRIMARY KEY AUTO_INCREMENT,
            Task_name VARCHAR(255) NOT NULL,
            Task_description TEXT NOT NULL,
            Task_state ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
            Creation_date DATE NOT NULL DEFAULT (CURRENT_DATE)
            );
        """)
    cursor.close()


# funkce pro přídán názvu a popisku úkolu + ověření vstupu
# task_name a task_description jsou definované jako None z důvodu předání argumentů do automatizovaného testu - zůstane tím zachován i negativní test
def add_task(conn, task_name=None, task_description=None):
    if task_name is None:
        task_name = input("Zadejte název úkolu: ")
    if task_description is None:
        task_description = input("Zadejte popis úkolu: ")

    if not task_name or not task_description:
        print("\n❌ Chyba, název úkolu ani popisek nesmí být prázdný!\n")
    else:
        add_task_db(conn, task_name, task_description)

# funkce pro přidání úkolu do databáze
def add_task_db(conn, task_name, task_description):
    cursor = conn.cursor(buffered=True)
    cursor.execute("INSERT INTO Tasks (Task_name, Task_description) VALUES (%s, %s);", (task_name, task_description))
    print("\n✅ Úkol byl úspěšně uložen do databáze.\n")
    conn.commit()
    cursor.close()


def view_tasks(conn, tasks_filter):
    cursor = conn.cursor(buffered=True)
    while True:
        cursor.execute("SELECT * FROM Tasks")
        if cursor.fetchone() is not None:
            if tasks_filter == "1":
                cursor.execute("SELECT * FROM Tasks")
                for task in cursor.fetchall():
                    print(f'{task[0]} - {task[1]} - {task[2]} - {task[3]} - {task[4]}')
                break
            elif tasks_filter == "2":
                cursor.execute("SELECT * FROM Tasks WHERE Task_state = 'Probíhá'")
                for task in cursor.fetchall():
                    print(f'{task[0]} - {task[1]} - {task[2]} - {task[3]} - {task[4]}')
                cursor.execute("SELECT * FROM tasks WHERE Task_state = 'Nezahájeno'")
                for task in cursor.fetchall():
                    print(f'{task[0]} - {task[1]} - {task[2]} - {task[3]} - {task[4]}')
                break    
            else:
                print('\n❌ Neplatný výběr filtru.\n')
                continue
        else:
            print('\nDatabáze je prázdná.\n')
            break

    cursor.close()


# funkce pro aktualizaci stavu úkolu + ověření chybného výběru
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

# funkce pro zobrazení hlavního menu s výběrem ze 4 možností + volání vybrané funkce
def main_menu(conn):
    while True:
        print("Správce úkolů - hlavní menu\n1. Přidat nový úkol\n2. Zobrazit všechny úkoly\n3. Aktualizovat úkol \n4. Odstranit úkol\n5. Konec programu")
        function_selection = input("Vyberte možnost (1-5): ")
        
        if function_selection == "1":
            add_task(conn)
        elif function_selection == "2":
            tasks_filter = input("Vyberte úkoly, které chcete zobrazit:\n1.Zobrazit všechny úkoly.\n2.Zobrazit pouze nedokončené úkoly.\nZvolený filtr: ")
            view_tasks(conn, tasks_filter)
        elif function_selection == "3":
            view_tasks(conn, tasks_filter = "2")
            choosen_task = input("Zadejte ID úkolu, který chcete aktualizovat: ")
            choosen_state = input("Vyberte stav, který chcete úkolu přiřadit:\n1. Probíhá\n2. Hotovo\nVybraný stav: ")
            update_task(conn, choosen_task, choosen_state)
        elif function_selection == "4":
            view_tasks(conn, tasks_filter = "1")
            choosen_task = input("Zadejte ID úkolu, který chcete smazat: ")
            delete_task(conn, choosen_task)
        elif function_selection == "5":
            print("Konec programu.")
            conn.close()
            break
        else:
            print("Byla vybrána neplatná funkce. Zadejte prosím platnou možnost: ")

# načtení credentials z .env
load_dotenv()

# Ověření, zda došlo k úspěšnému připojení. Podkud ano, spustí se funkce pro vytvoření tabulky a spuštění hlavního menu.
if __name__ == '__main__':
    conn = connection()
    if conn is not None:
        create_table(conn)
        main_menu(conn)
    else:
        print("Připojení selhalo")