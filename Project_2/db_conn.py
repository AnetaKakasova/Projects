import mysql.connector
from mysql.connector.connection import MySQLConnection

def connection() ->MySQLConnection:
    conn = mysql.connector.connect(
        host="localhost"
        user="root"
        password="1111"
        database="tasks"
        )
    return conn