from os.path import abspath, dirname, join as path_join, split
import sqlite3


class Database:

    __database_name = "production.db"
    __database_init = "init.sql"

    def __init__(self, database: str = __database_name):
        self.base_dir = split(dirname(abspath(__file__)))[0]
        self.db_path = path_join(self.base_dir, "databases", database)
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

    def init_db(self) -> None:
        init_file = path_join(self.base_dir, "databases", self.__database_init)
        with open(init_file, "r") as f:
            queries = f.read()
            self.cur.executescript(queries)

    def drop_db(self):
        self.cur.executescript("""
        BEGIN TRANSACTION;
            DROP TABLE IF EXISTS lottery;
            DROP TABLE IF EXISTS draw_schedule;
        END;
        """)
