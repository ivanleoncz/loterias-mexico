import os

from dotenv import load_dotenv

from modules.database import Database
from modules.etl import ETL
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
        assert len(result.fetchall()) == 3

    def test_web_scrapping(self):

        # Preparing environment variables
        load_dotenv()
        os.environ["LOTERIA_NACIONAL_URL"] = "https://gist.githubusercontent.com/ivanleoncz/"
        os.environ["LOTERIA_NACIONAL_URL_TRIS"] = (
                f"{os.environ['LOTERIA_NACIONAL_URL']}" +
                "/f0bc20813ac7b44c83d110c853c2e282/raw/6e99b3fcbf50506e8f1210373464694af0427d22/"
                "loteria_nacional_tris.html")

        # Numbers taken from LOTERIA_NACIONAL_URL_TRIS dataset
        lottery_initial_draw = 29873
        lottery_gist_dataset_amount_of_draws = 1915

        # Insert draw data, faking as it was the latest draw data available on the database
        self.db.cur.execute("""INSERT INTO draw (lottery_id, number, r1, r2, r3, r4, r5)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""", (60, lottery_initial_draw, 0, 9, 9, 2, 3))

        # Test presence of the last draw
        db_result = self.db.cur.execute("""SELECT * FROM draw""").fetchall()
        assert len(db_result) == 1

        # Test ETL process (ensure equality between dataset draws and database)
        etl = ETL(self.db)
        etl.download(lottery_id=os.environ["LOTERIA_NACIONAL_ID_TRIS"])
        assert len(self.db.cur.execute("""SELECT * FROM draw""").fetchall()) == lottery_gist_dataset_amount_of_draws

    def test_drop_db(self):
        self.__class__.db.drop_db()
        result = self.__class__.db.cur.execute(""" SELECT name FROM sqlite_master; """)
        assert len(result.fetchall()) == 0
