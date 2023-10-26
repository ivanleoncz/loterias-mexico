
def prepare_dataframe_tris(df):
    """
    Returns filtered version, with columns of interest and data transformations (if necessary).
    """
    df.rename(columns={"R1": "C1", "R2": "C2", "R3": "C3", "R4": "C4", "R5": "C5", }, inplace=True)
    return df[['C1', 'C2', 'C3', 'C4', 'C5', 'FECHA']]


def prepare_dataframe_melate_retro(df):
    """
    Returns filtered version, with columns of interest and data transformations (if necessary).
    """
    df.rename(columns={"F1": "C1", "F2": "C2", "F3": "C3", "F4": "C4", "F5": "C5", "F6": "C6", "F7": "C7", },
              inplace=True)
    return df[['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'BOLSA', 'FECHA']]


def filter_dataframe_by_year(df, year="2023"):
    """
    Returns dataset filtered by year.
    """
    return df.loc[df["FECHA"].str.contains(str(year))]


def get_numbers_probability_per_column(df) -> dict:
    """
    Count the draws of a number per column and the percentage which it corresponds, based on all lottery draws.
    """
    columns = dict()
    df_size = len(df)

    for column in df.columns:
        columns[column] = {k: [v, (int(v) * 100) / df_size] for k, v in dict(df[column].value_counts()).items()}

    return columns
