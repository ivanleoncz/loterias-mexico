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
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

    INSERT INTO lottery (name) VALUES ('tris'), ('melate_retro');
    INSERT INTO draw_schedule (lottery_id, days) VALUES (1, 'everyday'), (2, 'tue,sat');

END;