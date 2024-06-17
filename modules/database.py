from os.path import join as path_join
import sqlite3

from .utils import BASE_DIR
from . import script_db_init, script_db_drop


class Database:

    __database_name = "production.db"

    def __init__(self, database: str = __database_name):
        self.db_path = path_join(BASE_DIR, "databases", database)
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()
        # status: not tested
        if not self.database_tables_present():
            self.init_db()

    def init_db(self) -> None:
        """
        Creates the necessary database tables. See modules/__init__.py for more information.
        """
        self.cur.executescript(script_db_init)

    def drop_db(self):
        """
        Creates the necessary database tables. See modules/__init__.py for more information.
        """
        self.cur.executescript(script_db_drop)

    def database_tables_present(self) -> bool:
        """
        Check if required database tables are present ot not.

        status: not tested
        """
        database_tables = self.cur.execute("""SELECT name FROM sqlite_master""").fetchall()
        if database_tables:
            return True
        return False
