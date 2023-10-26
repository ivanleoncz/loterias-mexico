import argparse
import json

import pandas as pd

from utils import prepare_dataframe_tris, prepare_dataframe_melate_retro, get_probability_of_numbers_per_column

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and analyze datasets from Mexico Lottery services.")
    parser.add_argument('--type', '-t', help="name of the lottery service", required=True,
                        choices=['tris', 'melate_retro'], )
    args = parser.parse_args()
    if args.type and args.type == 'tris':
        df = prepare_dataframe_tris(pd.read_csv('datasets/Tris.csv'))
        del df['FECHA']
        print(json.dumps(get_probability_of_numbers_per_column(df), indent=2, default=int))
    if args.type and args.type == 'melate_retro':
        df = prepare_dataframe_melate_retro(pd.read_csv('datasets/Melate-Retro.csv'))
        del df['FECHA']
        del df['BOLSA']
        print(json.dumps(get_probability_of_numbers_per_column(df), indent=2, default=int))