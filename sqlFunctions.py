#sqlFunctions.py

import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
    except Error as err:
        print(f'Error: "{err}"')

    return connection

def execute_query(connection, query, array):
    cursor = connection.cursor()
    try:
        cursor.execute(query)

        if array == 1:
            return cursor.fetchall()
        elif array == 2:
            return cursor.fetchone()

        connection.commit()
        print('Query successful')
    except Error as err:
        print(f'Error: "{err}"')
        return 0
