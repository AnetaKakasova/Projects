import pytest
import mysql.connector
from  Improved_task_manager import add_task, update_task, delete_task
from test__init__ import create_testing_table, data_teardown
from dotenv import load_dotenv
import os


load_dotenv()

@pytest.fixture(autouse= True)
def db_settup():
    create_testing_table()
    yield 
    data_teardown()

@pytest.fixture()
def testing_db_connection():
    return  mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="Test_task_manager"
    )


def test_positive_add_task(testing_db_connection):
    add_task(testing_db_connection, "Název tasku 1", "Popis tasku 1")

    cursor = testing_db_connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    result = list(cursor.fetchall())

    testing_db_connection.close()
    assert len(result) != 0


def test_negative_add_task(capsys, testing_db_connection):

    add_task(testing_db_connection,"","")
    captured = capsys.readouterr()

    testing_db_connection.close()
    assert captured.out.strip() == "❌ Chyba, název úkolu ani popisek nesmí být prázdný!"


def test_positive_update_task(testing_db_connection):

    add_task(testing_db_connection,"Název aktualizovaného tasku", "Popis aktualizovaného tasku")
    update_task(testing_db_connection,"1","2")

    cursor = testing_db_connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE Task_state = 'Hotovo'")
    result = list(cursor.fetchall())

    testing_db_connection.close()
    assert len(result) != 0

def test_negative_update_task(capsys,testing_db_connection):
    update_task(testing_db_connection,"1","3")
    captured = capsys.readouterr()

    testing_db_connection.close()
    assert captured.out.strip() == "❌ Chybná volba nového stavu."


def test_positive_delete_task(testing_db_connection):

    add_task(testing_db_connection, "Task pro smazani", "Testování smazání úkolu")
    delete_task(testing_db_connection,"1")

    cursor = testing_db_connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE TaskID = 1")
    result = list(cursor.fetchall())

    testing_db_connection.close()    
    assert len(result) == 0


def test_negative_delete_task(capsys,testing_db_connection):

    delete_task(testing_db_connection,"15")
    captured = capsys.readouterr()

    testing_db_connection.close()
    assert captured.out.strip() == "❌ Byl vybrán neexistující úkol!"