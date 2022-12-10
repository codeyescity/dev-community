import mysql.connector
from mysql.connector import Error
import settings
"""
try:
    connection = mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
    if connection.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print(e)
"""
def runSQL(sql, args = None):

    try:
        connection = mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)

    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql,args)

    result = cursor.fetchall()

    connection.commit()
    cursor.nextset()

    return result
