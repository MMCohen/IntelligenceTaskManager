import mysql.connector
from mysql.connector.aio import connect


class ConnectionDB:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = "Intelligence_db"


    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )



if __name__ == "__main__":
    con = ConnectionDB()
    connector = con.get_connection()

    cursor = connector.cursor()
    cursor.execute("show databases;")
    data = cursor.fetchall()
    cursor.close()
    connector.close()

    print(data)

