from os.path import abspath, dirname, split

BASE_DIR = split(dirname(abspath(__file__)))[0]

BUTTON_TEXT = "resultados anteriores"
DATASET_DIR = "datasets"
DATASET_TRIS = f"{DATASET_DIR}/Tris.csv"
DATASET_MELATE_RETRO = f"{DATASET_DIR}/MelateRetro.csv"
URL_DOMAIN = "https://loterianacional.gob.mx"
URL_TRIS = f"{URL_DOMAIN}/Tris/Resultados"
URL_MELATE_RETRO = f"{URL_DOMAIN}/MelateRetro/Resultados"
ID_TRIS = 60
ID_MELATE_RETRO = 30
TABLE_LOTTERY = "lottery"
TABLE_DRAW = "draw"

SQL_SCRIPT_DB_INIT = f"""
BEGIN TRANSACTION;

    DROP TABLE IF EXISTS {TABLE_LOTTERY};
    DROP TABLE IF EXISTS {TABLE_DRAW};

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

    INSERT INTO {TABLE_LOTTERY} (id, name) VALUES (60, 'tris'), (30, 'melate_retro');

END;
"""

SQL_SCRIPT_DB_DROP = f"""
BEGIN TRANSACTION;
    DROP TABLE IF EXISTS {TABLE_LOTTERY};
    DROP TABLE IF EXISTS {TABLE_DRAW};
END;        
"""
