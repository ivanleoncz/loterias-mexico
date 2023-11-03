import matplotlib.pyplot as plt
from numpy import nan
from pandas import to_datetime


def convert_date_column(df):
    """
    Convert date in string formats into actual Pandas date objects.
    """
    df["FECHA"] = to_datetime(df["FECHA"], dayfirst=True)
    return df


def convert_to_int64(df):
    """
    Convert Nan (not-a-number) and Float64 types (if any) to int64.
    """
    for col in df.columns:
        df[col] = df[col].replace(nan, -1)
        if df[col].dtypes == 'float64':
            df[col] = df[col].astype('int64')
    return df


def prepare_dataframe_tris(df):
    """
    Returns filtered version, with columns of interest (renaming) and data transformations (if necessary).
    """
    df = convert_to_int64(convert_date_column(df))
    df.rename(columns={"R1": "C1", "R2": "C2", "R3": "C3", "R4": "C4", "R5": "C5", }, inplace=True)
    return df[['C1', 'C2', 'C3', 'C4', 'C5', 'FECHA']]


def get_columns_of_drawn_numbers(df) -> list:
    """
    Returns a list of columns which contain drawn numbers.
    It depends on the execution of prepare_dataframe functions.
    """
    return [col for col in df.columns if col.startswith('C')]


def filter_columns_of_drawn_numbers(df, columns_filter: str = None) -> list:
    cols = get_columns_of_drawn_numbers(df)
    if columns_filter == "first":
        return [cols[0]]
    elif columns_filter == "second":
        return [cols[1]]
    elif columns_filter == "third":
        return [cols[2]]
    elif columns_filter == "fourth":
        return [cols[3]]
    elif columns_filter == "fifth":
        return [cols[4]]
    elif columns_filter == "starting_pair":
        return cols[:2]
    elif columns_filter == "first_three":
        return cols[:3]
    elif columns_filter == "first_four":
        return cols[:4]
    elif columns_filter == "last_four":
        return cols[-4:]
    elif columns_filter == "last_three":
        return cols[-3:]
    elif columns_filter == "ending_pair":
        return cols[-2:]
    elif columns_filter == "first_last":
        return [cols[0], cols[-1]]
    elif columns_filter == "second_penultimate":
        return [cols[1], cols[-2]]
    else:
        return cols


def count_drawn_numbers(df, columns_filter=None, sort_by_number: bool = False) -> dict:
    """
    Merge columns of selected drawn numbers and count their drawns.
    """
    cols = filter_columns_of_drawn_numbers(df, columns_filter)
    df = df[cols].astype('str').agg(''.join, axis=1).value_counts()
    if sort_by_number:
        return dict(df.sort_values())
    return dict(df)


def prepare_dataframe_melate_retro(df):
    """
    Returns filtered version, with columns of interest and data transformations (if necessary).
    """
    df = convert_date_column(df)
    df.rename(columns={"F1": "C1", "F2": "C2", "F3": "C3", "F4": "C4", "F5": "C5", "F6": "C6", "F7": "C7", },
              inplace=True)
    return df[['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'BOLSA', 'FECHA']]


def filter_dataframe_by_year(df, year: str = "2023"):
    """
    Returns dataset filtered by year.
    """
    return df.loc[(df["FECHA"] < f"{str(int(year) + 1)}-01-01") & (df["FECHA"] >= f"{year}-01-01")]


def get_numbers_probability_per_column(df, with_percentages=False) -> dict:
    """
    Count the draws of a number per column and the percentage which it corresponds, based on all lottery draws.
    """
    columns = dict()
    df_size = len(df)

    for column in filter_columns_of_drawn_numbers(df):
        numbers_and_draws = dict(df[column].value_counts()).items()
        if with_percentages:
            columns[column] = {int(k): [v, (int(v) * 100) / df_size] for k, v in numbers_and_draws}
        else:
            columns[column] = {int(k): v for k, v in numbers_and_draws}

    return columns


def get_numbers_probability_in_all_columns(df) -> dict:
    """
    Calculates probability of a number globally, not strict to a column, performing incremental sums of value_counts
    series of each column.
    """
    numbers = df['C1'].value_counts()  # initializing Series of number counters with the 1st column
    for column in filter_columns_of_drawn_numbers(df)[1:]:
        numbers += df[column]
    return dict(numbers)


def plot_probabilities(ds: dict, lottery=None):
    """
    Plotting bar chars of probabilities of each number per column.
    """
    base_title = "Probability of Drawn Numbers per Column"
    title = f'{base_title} on "{lottery}" lottery' if lottery else base_title
    fig, axes = plt.subplots(nrows=len(ds.keys()), ncols=1, figsize=(10, 10))
    axis = 0
    for col in ds:
        axes[axis].bar(ds[col].keys(), ds[col].values())
        axis += 1
    fig.suptitle(title)
    plt.subplots_adjust(hspace=0.3)
    plt.setp(axes, xticks=range(1, 40) if "Melate" in lottery else range(10))
    plt.show()
