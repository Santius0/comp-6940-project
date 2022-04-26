import os
import glob
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
from functools import wraps
from timeit import default_timer
import math
import json


def all_day_in_year(day=0, year=date.today().year):
    """Returns every occurrence of a specified weekday in a specified year"""

    # yyyy mm dd
    # 0 = mon 1 = tue 2 = wed 3 = thu 4 = fri 5 = sat 6 = sun
    dte = date(year, 1, 1)
    dte += timedelta(days=(day - dte.weekday()) % 7)
    while dte.year == year:
        yield dte
        dte += timedelta(days=7)


def files_in_path(path):
    return glob.glob(path)


def merge_csvs_in_path(path, glob_pattern="hot-100_*.csv", output_path='../data/billboard',
                       output_filename='merged_csv', index=False):
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


def execution_time(round_to=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            st = default_timer()
            ret = func(*args, **kwargs)
            et = default_timer()
            print(f"\n func:{func.__name__} args:[{args}, {kwargs}] took: {round(et - st, round_to)} sec")
            return ret

        return wrapper

    return decorator


def sigmoid(x: int or float) -> int or float:
    return 1 / (1 + math.exp(-x))


def tanh(x: int or float) -> int or float:
    return (2 * sigmoid(2 * x)) - 1


def squiggle(rank_counts: np.ndarray or list, ranks: np.ndarray or list, scaled: bool = True) -> int or float:
    assert(len(rank_counts) == len(ranks))
    s = 0
    for i in range(len(rank_counts)):
        s += rank_counts[i] * ranks[i]
    # print(s)
    # print(tanh(s))
    return tanh(s) if scaled else s


def rank_score_basic(rank: int) -> float:
    return 1/rank


def rank_score_classic(peak: int, rank: int) -> float:
    base = 101
    peak = base - peak
    rank = base - rank
    return peak - rank + 1


def rank_score_01(peak: int, rank: int) -> float:
    try:
        return abs(1 / (1 / peak + 1 / rank - 1))
    except ZeroDivisionError:  # when peak rank and current rank are 2 this happens.
                               # take the middle of rank+1 and rank-1
        return (abs(1 / (1 / peak + 1 / (rank + 1) - 1)) + abs(1 / (1 / peak + 1 / (rank - 1) - 1))) / 2


def rank_score_02(peak: int, rank: int) -> float:
    return 1 / (peak + rank - 1)


def col_by_name(df: pd.DataFrame, col_name: str) -> int:
    return df.columns.get_loc(col_name)


def load_mfcc_data(json_path=os.path.abspath("../data/audio/mffcs.json")):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return np.array(data['mfccs']), np.array(data['billboard_names'])
