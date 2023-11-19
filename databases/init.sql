BEGIN TRANSACTION;

    DROP TABLE IF EXISTS lottery;
    DROP TABLE IF EXISTS draw_schedule;

    PRAGMA foreign_keys = ON;

    CREATE TABLE lottery (
        id INTEGER PRIMARY KEY,
        name VARCHAR(32) NOT NULL,
        last_download DATETIME
    );

    CREATE TABLE draw_schedule (
        id INTEGER PRIMARY KEY,
        lottery_id INTEGER NOT NULL,
        days VARCHAR(16) NOT NULL,
        hours VARCHAR(16) NOT NULL,
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

END;