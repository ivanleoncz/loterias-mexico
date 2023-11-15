import sqlite3


class Database:

    __database_name = "loterias_mexico.db"

    def __init__(self):
        self.con = sqlite3.connect(self.__class__.__database_name)
        self.cur = self.con.cursor()
