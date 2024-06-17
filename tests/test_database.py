import os

from dotenv import load_dotenv

from modules.database import Database
from modules.etl import ETL
from modules.utils import BASE_DIR


class TestDatabase:
    """
    Testing database consistency, based on ETL processes, including web-scrapping against Github Gist files,
    in order to avoid possible IP bans, due to subsequent testing executions.

    Two Gist files are used on these tests, in order to not use Mexico's Loteria Nacional service, avoiding a possible
    IP ban, in case that too much tests (requests) are executed: one Gist contains the HTML code of Mexico's Loteria
    Nacional for "Tris" lottery product, with a link/button pointing to ANOTHER Gist file, which is the CSV dataset that
    contains a small set of draws, just as it happens when normally using the original website, downloading lottery
    results.
    """

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
        """
        Tests database initialization.
        """
        assert len(self.__class__.db.cur.execute(""" SELECT name FROM sqlite_master; """).fetchall()) == 3

    def test_etl(self):
        """
        Tests ETL processing, downloading data (web-scrapping) against Gist files
        and loading the data into the database.
        """

        # From Gist file (LOTERIA_NACIONAL_URL_TRIS -> .csv)
        gist_first_draw = 29873  # last record
        gist_amount_of_draws = 1915  # counting the last record

        # Preparing environment variables, using URLs from Gist files (mocking web-scrapping).
        load_dotenv()
        os.environ["LOTERIA_NACIONAL_URL"] = "https://gist.githubusercontent.com/ivanleoncz/"
        os.environ["LOTERIA_NACIONAL_URL_TRIS"] = (
                f"{os.environ['LOTERIA_NACIONAL_URL']}" +
                "/f0bc20813ac7b44c83d110c853c2e282/raw/6e99b3fcbf50506e8f1210373464694af0427d22/"
                "loteria_nacional_tris.html")

        # Insert draw data, faking as it was the latest draw data available on the database
        self.db.cur.execute("""INSERT INTO draw (lottery_id, number, r1, r2, r3, r4, r5)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""", (60, gist_first_draw, 0, 9, 9, 2, 3))

        # Test presence of the last draw
        assert len(self.db.cur.execute("""SELECT * FROM draw""").fetchall()) == 1

        # Test draws database update via ETL process, ensuring equality between dataset and database
        etl = ETL(self.db)
        etl.download(lottery_id=os.environ["LOTERIA_NACIONAL_ID_TRIS"])
        assert len(self.db.cur.execute("""SELECT * FROM draw""").fetchall()) == gist_amount_of_draws

    def test_drop_db(self):
        """
        Tests database drop method: its regular use is not expected, even though the function exists.
        """
        self.__class__.db.drop_db()
        result = self.__class__.db.cur.execute(""" SELECT name FROM sqlite_master; """)
        assert len(result.fetchall()) == 0
