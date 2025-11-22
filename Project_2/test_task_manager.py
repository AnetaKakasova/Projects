import pytest
import mysql.connector
from  Improved_task_manager import add_task, view_tasks, update_task, delete_task
from test__init__ import create_testing_table, data_teardown


@pytest.fixture(autouse= True)
def db_settup():
    create_testing_table()
    yield 
    data_teardown()

@pytest.fixture()
def testing_db_connection():
    return  mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="task_manager_test"
    )
    
@pytest.fixture()
def testing_db_connection_for_units():
    return  mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="task_manager_test"
    )

@pytest.fixture()
def testing_db_connection_for_sub_units():
    return  mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="task_manager_test"
    )


def test_positive_add_task(testing_db_connection, testing_db_connection_for_units):
    add_task(testing_db_connection_for_units, "Název pro task - 1", "Popis tasku - 1")

    cursor = testing_db_connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    result = list(cursor.fetchall())

    testing_db_connection.close()
    assert len(result) != 0


def test_negative_add_task(capsys, testing_db_connection, testing_db_connection_for_units):

    add_task(testing_db_connection_for_units,"","")
    captured = capsys.readouterr()

    testing_db_connection.close()
    assert captured.out.strip() == "❌ Chyba, název úkolu ani popisek nesmí být prázdný!"