import pandas as pd
import numpy as np
import networkx as nx
import statsmodels.api as sm
import sqlite3
import os
import re
import seaborn as sns
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from itertools import combinations

import warnings
warnings.filterwarnings('ignore')

from utils import ROOTPATH, build_df_year, generate_index
from backbone import disparity_filter


def load_data():
    dfall = pd.DataFrame()
    for y in range(2012, 2016):
        dfyear = build_df_year(y, with_text=False, with_time=False, filter_null=True)
        dfall = dfall.append(dfyear)
    return dfall

def aggr_df(df):
    print("aggregating dataframe...")
    aggr_func = {
        "subreddit": lambda x: set(x),
        "submission_id": lambda x: set(x),
        "uniq_id":lambda x: list(x)
                }
    dfall["uniq_id"] = range(0, len(dfall))
    user_aggr = dfall.groupby("author").agg(aggr_func)  # this should take a while
    user_aggr = user_aggr.reset_index()
    user_aggr["n_subr"] = user_aggr["subreddit"].map(lambda x: len(x))
    user_aggr["n_subm"] = user_aggr["submission_id"].map(lambda x: len(x))
    user_aggr["n_post"] = user_aggr["uniq_id"].map(lambda x: len(x))
    return user_aggr

def write_active_userls(aggr_df, min_subr=2, min_subm=2, min_post=10):
    print("writing user lists...")
    user_select = aggr_df[(aggr_df["n_subm"]>=min_subm)&(aggr_df["n_post"]>=min_post)&(aggr_df["n_subr"]>=min_subr)][["author"]]
    user_select.to_csv(ROOTPATH + f"indx/ACTIVEUSERS_ALLYEARS_{min_subr}_{min_subm}_{min_post}.csv", index=False)

if __name__ == "__main__":
    print("loading data...")
    dfall = load_data()
    aggr = aggr_df(dfall)
    for x in [10, 20, 50, 100]:
        write_active_userls(aggr, min_subm=10, min_post=x)
