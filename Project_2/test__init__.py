import mysql.connector

def create_testing_table():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="task_manager_test"
    )

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks")

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


def data_teardown():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="task_manager_test"
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks")

if __name__ == '__main__':
    create_testing_table()