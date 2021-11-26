import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import sqlite3


ROOTPATH = os.getcwd()[:-3]
DBPATH1 = "/Users/yijingch/Documents/MYDATA/mobility/reddit-db-2012-2015.db"
conn1 = sqlite3.connect(DBPATH1)
# cur1 = conn.cursor()


def build_subm_df(year, with_text=True):
    print("- fetching submissions for year", year)
    if with_text:
        qr = f"SELECT id AS submission_id, author, title, selftext, subreddit, toxicity FROM 'submission-{year}' "
        qr += f"WHERE author != '[deleted]' "
        qr += f"AND (title != '' OR selftext != '')"
        df = pd.read_sql_query(qr, conn1)
        df["body"] = df["title"] + " " + df["selftext"]
        df = df.drop(columns=["title", "selftext"])
    else:
        qr = f"SELECT id AS submission_id, author, title, subreddit, toxicity FROM 'submission-{year}' "
        qr += f"WHERE author != '[deleted]'"
        df = pd.read_sql_query(qr, conn1)
    return df


def build_comm_df(year, with_text=True):
    print("- fetching comments for year", year)
    if with_text:
        qr = f"SELECT id AS comment_id, link_id AS submission_id, parent_id, author, body, subreddit, toxicity FROM 'comment-{year}' "
    else:
        qr = f"SELECT id AS comment_id, link_id AS submission_id, parent_id, author, body, subreddit, toxicity FROM 'comment-{year}' "
    qr += f"WHERE author != '[deleted]' "
    qr += f"AND body != ''"
    df = pd.read_sql_query(qr, conn1)
    df["submission_id"] = df["submission_id"].map(lambda x: x[3:])
    return df


def build_df_year(year):
    global USERS, SUBREDDITS
    print(f"building base dataframe for year {year}...")
    subm_df = build_subm_df(year)
    comm_df = build_comm_df(year)
    df_year = pd.concat([subm_df,comm_df])
    USERS = df_year.author.unique()
    SUBREDDITS = df_year.subreddit.unique()
    return df_year


def generate_index():
    global subr2index, index2subr, index2user, user2index
    subr2index = index2subr = index2user = user2index = {}

    for i,s in enumerate(SUBREDDITS):
        subr2index[s.lower()] = i
        index2subr[i] = s.lower()
    for i,u in enumerate(USERS):
        user2index[u] = i
        index2user[i] = u


def build_user_graph(dfyear):
    user_aggr = dfyear.groupby("author").agg({"subreddit": lambda x: set(list(x))}).reset_index()
    user





# def build_subr_graph():
#
#
# def build_subm_tree():
