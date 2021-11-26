## ---------------------------------- ##
## ---- Parse from raw JSON data ---- ##
## ---------------------------------- ##


from datetime import datetime
# from reset_db_gl import DBNAME, DBPATH, ROOT_PATH
import pandas as pd
import numpy as np
import argparse
import sqlite3
import ijson
import json
import os


ROOT_PATH = os.getcwd()[:-4]
DBNAME = "reddit-db-new.db"
DBPATH = ROOT_PATH + f"/data/{DBNAME}"
# DESC_FILE = ROOT_PATH + "/data/index/descriptives-from-2012.csv"

INVALID_TEXT = ["[deleted]", "[removed]", "\n"]

def load_subreddit(filepath = ROOT_PATH + "/data/index/left-right-labels.csv"):
    data = pd.read_csv(filepath)
    subreddit_ls = data.subreddit.tolist()
    return subreddit_ls


def fetch_data(colname, jsondata):
    try: output = jsondata[colname]
    except: output = ""
    return output


def fetch_json(folder_name, start_year, end_year):  # ok!
    """
    -------------------------------------------------
    input folder structure:
      data
        |--- raw
        |     |--- comment-from-2012
        |     |      |--- 2012
        |     |      |     |--- comm_subreddit1_2012.json
        |     |      |     |--- comm_subreddit2_2012.json
        |     |      |     |--- ...
        |     |      |     |--- comm_subreddiN_2012.json
        |     |      |--- 2013
        |     |      |--- ...
        |     |      |--- 2020
        |     |--- submission-from-2012
        |     |      |--- 2012
        |     |      |     |--- subm_subreddit1_2012.json
        |     |      |     |--- subm_subreddit2_2012.json
        |     |      |     |--- ...
        |     |      |     |--- subm_subredditN_2012.json
        |     |      |--- 2013
        |     |      |--- ...
        |     |      |--- 2020
    -------------------------------------------------
    ACTION: fetch a list of json filepath (not only filename)
    """
    json_files_all = []
    json_files_year = []
    for year in [*range(start_year, end_year)]:
        json_files_year = os.listdir(f"{ROOT_PATH}/data/raw/{folder_name}/{year}")
        # json_files_year = [f"{ROOT_PATH}/data/raw/{folder_name}/{year}" + "/" + x for x in json_files_year]
        json_files_all += json_files_year
    # print(json_files_all)

    return json_files_all


def parse_subm_data(filepath):
    with open(filepath) as jsonf:
        data = json.load(jsonf)

    id_ls = []
    author_ls = []
    author_fullname_ls = []
    subreddit_ls = []
    title_ls = []
    selftext_ls = []
    score_ls = []
    created_utc_ls = []

    for d in data:
        if fetch_data("selftext", d) not in INVALID_TEXT:
            id_ls.append(fetch_data("id", d))
            author_ls.append(fetch_data("author", d))
            author_fullname_ls.append(fetch_data("author_fullname", d))
            subreddit_ls.append(fetch_data("subreddit", d))
            title_ls.append(fetch_data("title", d))
            selftext_ls.append(fetch_data("selftext", d).strip())
            score_ls.append(fetch_data("score", d))
            created_utc_ls.append(fetch_data("created_utc", d))

    subm_df = pd.DataFrame()
    subm_df["id"] = id_ls
    subm_df["author"] = author_ls
    subm_df["author_fullname"] = author_fullname_ls
    subm_df["subreddit"] = subreddit_ls
    subm_df["title"] = title_ls
    subm_df["selftext"] = selftext_ls
    subm_df["score"] = score_ls
    subm_df["created_utc"] = created_utc_ls

    return subm_df


def parse_comm_data(filepath):
    with open(filepath) as jsonf:
        data = json.load(jsonf)

    id_ls = []
    author_ls = []
    author_fullname_ls = []
    subreddit_ls = []
    parent_id_ls = []
    link_id_ls = []
    body_ls = []
    score_ls = []
    created_utc_ls = []

    for d in data:
        if fetch_data("body", d) not in INVALID_TEXT:
            id_ls.append(fetch_data("id", d))
            author_ls.append(fetch_data("author", d))
            author_fullname_ls.append(fetch_data("author_fullname", d))
            subreddit_ls.append(fetch_data("subreddit", d))
            parent_id_ls.append(fetch_data("parent_id", d))
            link_id_ls.append(fetch_data("link_id", d))
            body_ls.append(fetch_data("body",d))
            score_ls.append(fetch_data("score", d))
            created_utc_ls.append(fetch_data("created_utc", d))

    comm_df = pd.DataFrame()
    comm_df["id"] = id_ls
    comm_df["author"] = author_ls
    comm_df["author_fullname"] = author_fullname_ls
    comm_df["subreddit"] = subreddit_ls
    comm_df["parent_id"] = parent_id_ls
    comm_df["link_id"] = link_id_ls
    comm_df["body"] = body_ls
    comm_df["score"] = score_ls
    comm_df["created_utc"] = created_utc_ls

    return comm_df


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--submission_folder", help="Name of the folder that stores raw submission data", type=str, default="submission-from-2016", required=False)
    argparser.add_argument("--comment_folder", help="Name of the folder that stores raw comment data", type=str, default="comment-from-2016", required=False)
    argparser.add_argument("--start_year", help="Start parsing from this year", type=int, default=2012, required=False)
    argparser.add_argument("--end_year", help="Start parsing from this year", type=int, default=2021, required=False)

    args = argparser.parse_args()
    submission_folder = args.submission_folder
    comment_folder = args.comment_folder

    # connect to db
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()

    print("""
    ********** ********** ********** ********** **********
                    PARSING SUBMISSIONS
    ********** ********** ********** ********** **********
    """)

    print("1. fetching submission json files...")
    submission_jsons = fetch_json(folder_name=submission_folder, start_year=args.start_year, end_year=args.end_year)
    print("  number of files:", len(submission_jsons), "\n")

    print("2. parsing json iterable objects...")
    index = 1
    for js_fname in submission_jsons:
        subrname = js_fname[5:-10]
        year = int(js_fname[-9:-5])

        print("  processing file:", f"{index}/{len(submission_jsons)}", "-", js_fname)
        json_fpath = f"{ROOT_PATH}/data/raw/{submission_folder}/{year}/{js_fname}"
        subm_df = parse_subm_data(json_fpath)
        subm_df.to_sql(f"submission-{year}", conn, if_exists="append")
        print(f"add to SQLITE TABLE submission-{year}")
        index += 1

    print("""
    ********** ********** ********** ********** **********
                    PARSING COMMENTS
    ********** ********** ********** ********** **********
    """)

    print("1. fetching submission json files...")
    comment_jsons = fetch_json(folder_name=comment_folder, start_year=args.start_year, end_year=args.end_year)
    print("  number of files:", len(comment_jsons), "\n")

    print("2. parsing json iterable objects...")
    index = 1
    for js_fname in comment_jsons:
        subrname = js_fname[5:-10]
        year = int(js_fname[-9:-5])

        print("  processing file:", f"{index}/{len(comment_jsons)}", "-", js_fname)
        json_fpath = f"{ROOT_PATH}/data/raw/{comment_folder}/{year}/{js_fname}"
        comm_df = parse_comm_data(json_fpath)
        comm_df.to_sql(f"comment-{year}", conn, if_exists="append")
        print(f"add to SQLITE TABLE comment-{year}")
        index += 1


# test
# python3 parse_to_db.py --start_year=2016 --end_year=2017






##
