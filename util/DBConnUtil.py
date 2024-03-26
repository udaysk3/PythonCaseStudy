from .DBPropertyUtil import PropertyUtil
import pyodbc

class DBConnection:
    connection = None

    @staticmethod
    def getConnection():
        if DBConnection.connection is None:
            try:
                connection_string = PropertyUtil.getPropertyString()
                DBConnection.connection = pyodbc.connect(connection_string)
                print("Connected Successfully")
            except pyodbc.Error as ex:
                print(f"Error: {ex}")
        return DBConnection.connection

    def close_connection(self):
        if DBConnection.connection:
            DBConnection.connection.close()
            print("Connection closed.")
