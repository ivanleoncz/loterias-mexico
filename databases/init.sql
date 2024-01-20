BEGIN TRANSACTION;

    DROP TABLE IF EXISTS lottery;
    DROP TABLE IF EXISTS draw;
    DROP TABLE IF EXISTS draw_schedule;

    PRAGMA foreign_keys = ON;

    CREATE TABLE lottery (
        id INTEGER PRIMARY KEY,
        name VARCHAR(32) NOT NULL
    );

    CREATE TABLE draw (
        id INTEGER PRIMARY KEY,
        lottery_id INTEGER NOT NULL,
        number INTEGER NOT NULL,
        r1 INTEGER NULL,
        r2 INTEGER NULL,
        r3 INTEGER NULL,
        r4 INTEGER NULL,
        r5 INTEGER NULL,
        r6 INTEGER NULL,
        r7 INTEGER NULL,
        jackpot INTEGER NULL,
        processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

    CREATE TABLE draw_schedule (
        id INTEGER PRIMARY KEY,
        lottery_id INTEGER NOT NULL,
        days VARCHAR(16) NOT NULL,
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

    INSERT INTO lottery (name) VALUES ('tris'), ('melate_retro');
    INSERT INTO draw_schedule (lottery_id, days) VALUES (60, 'everyday'), (30, 'tue,sat');

END;