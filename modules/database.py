from os.path import join as path_join
import sqlite3

from .utils import BASE_DIR


class Database:

    __database_name = "production.db"
    __database_init = "init.sql"

    def __init__(self, database: str = __database_name):
        self.db_path = path_join(BASE_DIR, "databases", database)
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

    def init_db(self) -> None:
        init_file = path_join(BASE_DIR, "databases", self.__database_init)
        with open(init_file, "r") as f:
            queries = f.read()
            self.cur.executescript(queries)

    def drop_db(self):
        self.cur.executescript("""
        BEGIN TRANSACTION;
            DROP TABLE IF EXISTS lottery;
            DROP TABLE IF EXISTS draw;
            DROP TABLE IF EXISTS draw_schedule;
        END;
        """)
