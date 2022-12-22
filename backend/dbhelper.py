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
    result = None
    try:
        connection = mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql,args)

        result = cursor.fetchall()
        connection.commit()
        
    except Exception as e:
        print(e)

    return result

def runSQL_return_id(sql, args = None):
    id = None
    try:
        connection = mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql,args)

        id = cursor.lastrowid
        connection.commit()
        
    except Exception as e:
        print(e)

    return id

class Database():
    def __init__(self):
        try:
            self.connection =  mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(e)

    def runSQL(self, sql, args = None):
        try:
            self.cursor.execute(sql,args)

            result = self.cursor.fetchall()
            self.connection.commit()

        except Exception as e:
            print(e)

        return result