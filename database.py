import sqlite3


class Database:
    cursor = None

    def __init__(self):
        connection = sqlite3.connect('amazonDatabase.db')
        self.cursor = connection.cursor()
        self.createTable()

    def createTable(self):
        sql_create_table = """ CREATE TABLE IF NOT EXISTS amazon (
                                ID INTEGER PRIMARY KEY NOT NULL,
                                name text,
                                email text,
                                password text,
                                adres text,
                                proxy text,
                                port INTEGER,
                                path text,
                                IDK text
                            ); """
        self.cursor.execute(sql_create_table)


    def addToTable(self, lista):
        print(lista[1])
        try:
            self.cursor.execute(
                f"INSERT INTO amazon (name, email, password, adres, proxy,port, path, IDK) VALUES ('{lista[0]}','{lista[1]}', '{lista[2]}','{lista[3]}','{lista[4]}','{lista[5]}','{lista[6]}','{lista[7]}')")

            self.cursor.connection.commit()
        except:
            print("Niepoprawne dane! Spróbuj jeszcze raz")

    def delFromTable(self, ID):
        sqlQuery = f"DELETE FROM amazon WHERE ID='{ID}'"
        self.cursor.execute(sqlQuery)
        self.cursor.connection.commit()

    def getAllData(self):
        sqlQuery = "SELECT * FROM amazon"
        return self.cursor.execute(sqlQuery)

    def getRowData(self, ID):
        sqlQuery = f"SELECT * FROM amazon where ID='{ID}'"
        return self.cursor.execute(sqlQuery).fetchone()
    def getLastPort(self):
        sqlQuery = "SELECT port FROM amazon order by ID DESC LIMIT 1"
        port = self.cursor.execute(sqlQuery).fetchone()
        return port[0]
