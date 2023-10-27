import argparse
import json

import pandas as pd

from utils import (prepare_dataframe_tris, prepare_dataframe_melate_retro, filter_dataframe_by_year,
                   get_numbers_probability_per_column, get_numbers_probability)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and analyze datasets from Mexico Lottery services.")
    parser.add_argument('--type', '-t', help="name of the lottery service", required=True,
                        choices=['tris', 'melate_retro'], )
    parser.add_argument('--year', '-y', help="filter results by year",)
    parser.add_argument('--all_columns', '-a', help="perform calculation on all columns",
                        action='store_true')
    args = parser.parse_args()
    if args.type:
        if args.type == 'tris':
            df = prepare_dataframe_tris(pd.read_csv('datasets/Tris.csv'))
            if args.year:
                df = filter_dataframe_by_year(df, year=args.year)
            if args.all_columns:
                df = get_numbers_probability(df)
            else:
                df = get_numbers_probability_per_column(df)
            print(json.dumps(df, indent=2, default=int))
        if args.type == 'melate_retro':
            df = prepare_dataframe_melate_retro(pd.read_csv('datasets/Melate-Retro.csv'))
            if args.year:
                df = filter_dataframe_by_year(df, year=args.year)
            if args.all_columns:
                df = get_numbers_probability(df)
            else:
                df = get_numbers_probability_per_column(df)
            print(json.dumps(df, indent=2, default=int))
