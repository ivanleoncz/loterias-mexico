import os

from modules.database import Database
from modules.utils import BASE_DIR


class TestDatabase:

    db = None
    database = "tests.db"

    @classmethod
    def setup_class(cls):
        cls.db = Database(database=cls.database)

    @classmethod
    def teardown_class(cls):
        cls.db.drop_db()
        os.remove(os.path.join(BASE_DIR, "databases", cls.database))

    def test_init_db(self):
        self.__class__.db.init_db()
        result = self.__class__.db.cur.execute(""" SELECT name FROM sqlite_master; """)
        assert len(result.fetchall()) == 2

    def test_drop_db(self):
        self.__class__.db.drop_db()
        result = self.__class__.db.cur.execute(""" SELECT name FROM sqlite_master; """)
        assert len(result.fetchall()) == 0
