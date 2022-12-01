import mysql.connector
from mysql.connector import Error
import settings
from faker import Faker


fake = Faker()



def connect():
    """ Connect to MySQL database """
    #connection = None
    try:
        connection = mysql.connector.connect(host = settings.host, database = settings.database, user = settings.user, password = settings.password)
        if connection.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)
    return connection
    """
    cur = connection.cursor(dictionary=True)

    cur.execute("SELECT * FROM countrylanguage;")
    res = cur.fetchall()
    for row in res:
        print(row)
    """




if __name__ == '__main__':

    con = connect()
    cur = con.cursor(dictionary=True)
    fake = Faker()
    #cur.execute("SELECT  *  FROM countrylanguage;")
    #cur.fetchall()
    #cur.execute("""DROP TABLE posts;""")
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS posts
        (
            post_id INT AUTO_INCREMENT PRIMARY KEY, 
            user_id INT,
            type TEXT,
            title TEXT,
            description TEXT,
            code TEXT,
            number_likes INT,
            post_creation_date DATETIME
        );
    """
    );
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS users
        (
            user_id INT AUTO_INCREMENT PRIMARY KEY, 
            name TEXT
        );
    """
    );
    cur.execute("""INSERT INTO posts (description) VALUES (%s);""",(fake.text(),))
    con.commit()
    cur.execute("""INSERT INTO users (name) VALUES (%s);""",(fake.name(),))
    con.commit()

    res = cur.fetchall()
    for row in res:
        print(row)


