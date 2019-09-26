import sqlite3

class ConnectionFactory:
    def __init__(self,path):
        self.db_path = path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


