import os
import glob
import pandas as pd
from datetime import date, timedelta
import string


def all_day_in_year(day=0, year=date.today().year):
    """Returns every occurrence of a specified weekday in a specified year"""

    # yyyy mm dd
    # 0 = mon
    # 1 = tue
    # 2 = wed
    # 3 = thu
    # 4 = fri
    # 5 = sat
    # 6 = sun
    dte = date(year, 1, 1)
    dte += timedelta(days=(day - dte.weekday()) % 7)
    while dte.year == year:
        yield dte
        dte += timedelta(days=7)


def files_in_path(path):
    return glob.glob(path)


def merge_csvs_in_path(path, glob_pattern="hot-100_*.csv", output_path='../data/billboard', output_filename='merged_csv', index=False):
    files = glob.glob(f'{os.path.abspath(path)}/{glob_pattern}')
    full_df = None
    for file in files:
        full_df = pd.read_csv(file) if full_df is None else pd.concat([full_df, pd.read_csv(file)])
    full_df.to_csv(f"{output_path}/{output_filename}.csv", index=index)


def remove_punctuation(val: str) -> str:
    return val.translate(str.maketrans('', '', string.punctuation))


def mkdir(path: str) -> str:
    path = os.path.abspath(path)
    os.makedirs(path) if not os.path.exists(path) else None
    return path


def open_or_create_csv(path, cols):
    path = os.path.abspath(path)
    dir = os.sep.join(path.split(os.sep)[:-1])
    os.makedirs(dir) if not os.path.exists(dir) else None
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        pd.DataFrame(columns=cols).to_csv(path, index=False)
        return pd.read_csv(path)
