import argparse
import json

import pandas as pd

from utils import (prepare_dataframe_tris, prepare_dataframe_melate_retro, filter_dataframe_by_year,
                   get_probability_of_numbers_per_column, get_probability_of_numbers_in_all_columns, plot_probabilities,
                   count_winning_numbers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and analyze datasets from Mexico Lottery services.")
    parser.add_argument('--type', '-t', help="name of the lottery service", required=True,
                        choices=['tris', 'melate_retro'], )
    parser.add_argument('--year', '-y', help="filter results by year",)
    parser.add_argument('--all_columns', '-a', help="perform calculation on all columns",
                        action='store_true')
    parser.add_argument('--plot', '-p', help="plot results into Matplotlib chart",
                        action='store_true')
    parser.add_argument('--list', '-l', help="count and list winning numbers",
                        action='store_true')
    parser.add_argument('--combination', '-c',
                        help="count and list winning numbers based on combination of columns",
                        choices=['first', 'second', 'third', 'fourth', 'fifth', 'starting_pair', 'first_three',
                                 'first_four', 'last_four', 'last_three', 'ending_pair', 'first_last',
                                 'second_penultimate'])
    parser.add_argument('--sort_numbers', '-s',
                        help="sort --list and --combination results by drawn number", action="store_true")
    args = parser.parse_args()

    if args.type:

        df = None
        if args.type == 'tris':
            df = prepare_dataframe_tris(pd.read_csv('datasets/Tris.csv'))
        elif args.type == 'melate_retro':
            df = prepare_dataframe_melate_retro(pd.read_csv('datasets/Melate-Retro.csv'))

        if args.year:
            df = filter_dataframe_by_year(df, year=args.year)

        if args.all_columns:
            print(json.dumps(get_probability_of_numbers_in_all_columns(df), indent=2))
        else:
            data = get_probability_of_numbers_per_column(df)

            # Data presentation
            if args.plot:
                if args.type == 'tris':
                    plot_probabilities(ds=data, lottery="TRIS " + args.year if args.year else "")
                elif args.type == 'melate_retro':
                    plot_probabilities(ds=data, lottery="Melate Retro " + args.year if args.year else "")
            elif args.list:
                if args.sort_numbers:
                    result = count_winning_numbers(df, sort_by_number=True)
                else:
                    result = count_winning_numbers(df)
                print(json.dumps(result, indent=2, default=int))
            elif args.combination:
                if args.sort_numbers:
                    result = count_winning_numbers(df, combination=args.combination, sort_by_number=True)
                else:
                    result = count_winning_numbers(df, combination=args.combination)
                print(json.dumps(result, indent=2, default=int))
            else:
                print(df.head(10))
