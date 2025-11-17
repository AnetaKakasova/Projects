import mysql.connector
from mysql.connector.connection import MySQLConnection


def connection() ->MySQLConnection:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1111",
        database="task_manager"
        )
    print("Successfull")
    return conn



def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INT PRIMARY KEY AUTO_INCREMENT,
            Task_name VARCHAR(255) NOT NULL,
            Task_description TEXT NOT NULL
            );""")
    print("Created!")

def select(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from Tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)
    cursor.close()
    conn.close()
    print("Selected")

conn = connection()
create_table(conn)
select(conn)