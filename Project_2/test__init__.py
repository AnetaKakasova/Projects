import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# vytvoření testovací tabulky
def create_testing_table():
    conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Test_task_manager")
    conn.database = "Test_task_manager"

    cursor.execute("DROP TABLE IF EXISTS Tasks")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
                TaskID INT PRIMARY KEY AUTO_INCREMENT,
                Task_name VARCHAR(255) NOT NULL,
                Task_description TEXT NOT NULL,
                Task_state ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
                Creation_date DATE NOT NULL DEFAULT (CURRENT_DATE)
                );
        """) 
    conn.commit()
    cursor.close()
    conn.close()


# smazání testovací tabulky
def data_teardown():
    conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="Test_task_manager"
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Tasks")

if __name__ == '__main__':
    create_testing_table()