import mysql.connector
from mysql.connector.connection import MySQLConnection, Error

# vytvoření připojení k databázi
def pripojeni_db() ->MySQLConnection | None:
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
def vytvoreni_tabulky(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                TaskID INT PRIMARY KEY AUTO_INCREMENT,
                Task_name VARCHAR(255) NOT NULL,
                Task_description TEXT NOT NULL,
                Task_state ENUM('nezahájeno', 'probíhá', 'hotovo') NOT NULL DEFAULT 'nezahájeno',
                Creation_date DATE NOT NULL DEFAULT (CURRENT_DATE)
                );
            """)
    finally:
        cursor.close()
        conn.close()


# funkce pro zobrazení hlavního menu s výběrem ze 4 možností
def hlavni_menu():
    print("Správce úkolů - hlavní menu\n1. Přidat nový úkol\n2. Zobrazit všechny úkoly\n3. Aktualizovat úkol \n4. Odstranit úkol\n5. Konec programu")
    function = input("Vyberte možnost (1-5): ")
    return function 


# tato funkce slouží pro vložení nového úkolu
def pridat_ukol(conn):
    task_name = input("Zadejte název úkolu: ")
    task_description = input("Zadejte popis úkolu: ")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks (Task_name, Task_description) VALUES (%s, %s);", (task_name, task_description))
    conn.commit()
    cursor.close()
    conn.close()


# funkce pro zobrazení úkolů v databázi Tasks
def view_tasks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from Tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("Seznam úkolů je prázdný.")
    else:
        print("Seznam úkolů:")
        for task in tasks:
            print(task)
    cursor.close()
    conn.close()


# tato funkce je pro smazání úkolu
def delete_task(conn):
    task_deletion = int(input("Zadejte číslo úkolu, který chcete smazat: "))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE TaskID = %s;", (task_deletion,))
    conn.commit()
    cursor.close()
    conn.close()







while True:

    conn = pripojeni_db()
    vytvoreni_tabulky(conn)
    function_selection = hlavni_menu()
    

    if function_selection == "1":
        conn = pripojeni_db()
        pridat_ukol(conn)
    elif function_selection == "2":
        conn = pripojeni_db()
        view_tasks(conn)
    elif function_selection == "3":
        conn = pripojeni_db()
        delete_task(conn)
    elif function_selection == "4":
        conn = pripojeni_db()
        # aktualizovat_ukol(conn)
    elif function_selection == "5":
        exit("Konec programu.")
    else:
        print("Byla vybrána neplatná funkce. Zadejte prosím platnou možnost: ")
        continue