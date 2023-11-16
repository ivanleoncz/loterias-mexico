import sqlite3


class Database:

    __database_name = "loterias_mexico.db"

    def __init__(self, database : str = __database_name):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def init_db(self) -> None:
        self.cur.executescript("""
        BEGIN TRANSACTION;
        DROP TABLE IF EXISTS lottery;
        DROP TABLE IF EXISTS schedule_dow;
        DROP TABLE IF EXISTS schedule_hour;
        CREATE TABLE lottery (
            id INTEGER PRIMARY KEY,
            name VARCHAR(32) NOT NULL
        );
        CREATE TABLE schedule_dow (
            id INTEGER PRIMARY KEY,
            lottery_id INTEGER NOT NULL,
            dow VARCHAR(7) NOT NULL,
            FOREIGN KEY(lottery_id) REFERENCES lottery(id)
        );
        CREATE TABLE schedule_hour (
            id INTEGER PRIMARY KEY,
            schedule_dow_id INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            FOREIGN KEY(schedule_dow_id) REFERENCES schedule_dow(id)
        );
        END;
        """)

    def drop_db(self):
        self.cur.executescript("""
        BEGIN TRANSACTION;
        DROP TABLE IF EXISTS lottery;
        DROP TABLE IF EXISTS schedule_dow;
        DROP TABLE IF EXISTS schedule_hour;
        END;
        """)
