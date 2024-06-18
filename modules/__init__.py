TABLE_LOTTERY = "lottery"
TABLE_DRAW = "draw"
TABLE_SCHEDULE = "schedule"

SQL_SCRIPT_DB_INIT = f"""
BEGIN TRANSACTION;

    DROP TABLE IF EXISTS {TABLE_LOTTERY};
    DROP TABLE IF EXISTS {TABLE_DRAW};
    DROP TABLE IF EXISTS {TABLE_SCHEDULE};

    PRAGMA foreign_keys = ON;

    CREATE TABLE {TABLE_LOTTERY} (
        id INTEGER PRIMARY KEY,
        name VARCHAR(32) NOT NULL
    );

    CREATE TABLE {TABLE_DRAW} (
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

    CREATE TABLE {TABLE_SCHEDULE} (
        id INTEGER PRIMARY KEY,
        lottery_id INTEGER NOT NULL,
        available_on VARCHAR(16) NOT NULL,
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

    INSERT INTO {TABLE_LOTTERY} (id, name) VALUES (60, 'tris'), (30, 'melate_retro');
    INSERT INTO {TABLE_SCHEDULE} (lottery_id, available_on) VALUES (60, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'), (30, 'Wed,Sun');

END;
"""

SQL_SCRIPT_DB_DROP = f"""
BEGIN TRANSACTION;
    DROP TABLE IF EXISTS {TABLE_LOTTERY};
    DROP TABLE IF EXISTS {TABLE_DRAW};
    DROP TABLE IF EXISTS {TABLE_SCHEDULE};
END;        
"""
