import argparse
from datetime import datetime
import json

import pandas as pd

from modules import (DATASET_TRIS, DATASET_MELATE_RETRO, URL_TRIS, ID_TRIS, ID_MELATE_RETRO, URL_MELATE_RETRO,
                     URL_DOMAIN)
from modules.etl import LotteryETL
from modules.database import Database

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process and analyze datasets from Mexico Lottery services.")
    parser.add_argument('--type', '-t', help="name of the lottery service", required=True,
                        choices=['tris', 'melate_retro'], )
    parser.add_argument('--download', '-d', help="download dataset from Mexico's Loteria Nacional",
                        action='store_true')
    args = parser.parse_args()

    if args.type and args.download:

        db = Database()
        etl = LotteryETL(db)

        if args.type == 'tris':
            last_draw = etl.get_last_draw(ID_TRIS)
            if not last_draw or datetime.strptime(last_draw[1], "%Y-%m-%d %H:%M:%S").date() < datetime.now().date():
                etl.download(lottery_id=ID_TRIS, lottery_website=URL_DOMAIN, lottery_url=URL_TRIS,
                             lottery_dataset=DATASET_TRIS)
            else:
                print("INFO: TRIS results already downloaded today!")
        elif args.type == 'melate_retro':
            last_draw = etl.get_last_draw(ID_MELATE_RETRO)
            if not last_draw or datetime.strptime(last_draw[1], "%Y-%m-%d %H:%M:%S").date() < datetime.now().date():
                etl.download(lottery_id=ID_MELATE_RETRO, lottery_website=URL_DOMAIN, lottery_url=URL_MELATE_RETRO,
                             lottery_dataset=DATASET_MELATE_RETRO)
            else:
                print("INFO: MELATE RETRO results already downloaded today!")
