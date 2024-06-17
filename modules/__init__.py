lottery_table = "lottery"
draw_table = "draw"
schedule_table = "schedule"

script_db_init = f"""
BEGIN TRANSACTION;

    DROP TABLE IF EXISTS {lottery_table};
    DROP TABLE IF EXISTS {draw_table};
    DROP TABLE IF EXISTS {schedule_table};

    PRAGMA foreign_keys = ON;

    CREATE TABLE {lottery_table} (
        id INTEGER PRIMARY KEY,
        name VARCHAR(32) NOT NULL
    );

    CREATE TABLE {draw_table} (
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

    CREATE TABLE {schedule_table} (
        id INTEGER PRIMARY KEY,
        lottery_id INTEGER NOT NULL,
        available_on VARCHAR(16) NOT NULL,
        FOREIGN KEY(lottery_id) REFERENCES lottery(id)
    );

    INSERT INTO {lottery_table} (id, name) VALUES (60, 'tris'), (30, 'melate_retro');
    INSERT INTO {schedule_table} (lottery_id, available_on) VALUES (60, 'Mon,Tue,Wed,Thu,Fri,Sat,Sun'), (30, 'Wed,Sun');

END;
"""

script_db_drop = f"""
BEGIN TRANSACTION;
    DROP TABLE IF EXISTS {lottery_table};
    DROP TABLE IF EXISTS {draw_table};
    DROP TABLE IF EXISTS {schedule_table};
END;        
"""
