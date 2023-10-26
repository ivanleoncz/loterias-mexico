
def prepare_dataframe_tris(df):
    """
    Returns filtered version, with columns of interest and data transformations (if necessary).
    """
    df.rename(columns={"R1": "C1", "R2": "C2", "R3": "C3", "R4": "C4", "R5": "C5", })
    return df[['R1', 'R2', 'R3', 'R4', 'R5', 'FECHA']]


def prepare_dataframe_melate_retro(df):
    """
    Returns filtered version, with columns of interest and data transformations (if necessary).
    """
    df.rename(columns={"F1": "C1", "F2": "C2", "F3": "C3", "F4": "C4", "F5": "C5", "F6": "C6", "F7": "C7", })
    return df[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'BOLSA', 'FECHA']]


def filter_dataframe_by_year(df, year="2023"):
    """
    Returns dataset filtered by year.
    """
    return df.loc[df["FECHA"].str.contains(str(year))]


def get_probability_of_numbers_per_column(df) -> dict:

    columns = dict()

    for column in df.columns:
        columns[column] = dict(df[column].value_counts())

    return columns


