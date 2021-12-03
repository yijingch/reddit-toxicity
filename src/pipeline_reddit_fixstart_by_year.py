## ---------------------------------------------------- ##
## ---- crawl submissions and comments from Reddit ---- ##
## ---------------------------------------------------- ##


## unix time converter: https://www.unixtimestamp.com/index.php

import numpy as np
import pandas as pd
import argparse
import requests
from datetime import datetime
import time
import json
import csv
import re
import os

BASEURL = "https://api.pushshift.io/reddit/search/"
PATH = os.getcwd()[:-3]

def year2utc(year):
    dt = datetime(year, 1, 1)
    timestamp = int((dt - datetime(1970, 1, 1)).total_seconds())
    return timestamp


def utc2year(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    return int(dt.year)


def crawl_batches(subreddit, last_page = None, type = "", start_utc=0):
    """
    subreddit: subreddit name
    type: submission or comment
    -----------------------------
    action: crawl content of one year
    """
    start_year = utc2year(start_utc)
    end_utc = year2utc(start_year+1)


    params = {"subreddit":subreddit, "sort":"asc", "sort_type":"created_utc", "limit":1000, "after":start_utc, "before": end_utc}
    if last_page is not None:
        if len(last_page) > 0:
            params["after"] = last_page[-1]["created_utc"]  # resume from where we left at the last page
        else:
            return []
    output = requests.get(BASEURL + type, params = params)
    if not output.ok:
        raise Exception("Server returned status code {}".format(output.status_code))
    return output.json()["data"]


def crawl_submissions(subreddit, orig_start=2010, start_year=2010, end_year=2020):
    print(f"- Crawling submissions after {start_year}...")
    for y in range(start_year, end_year):
        submissions = []
        last_page = None
        batch = 1

        print(f" - year: {y}")
        start_utc = year2utc(y)

        while last_page != []:
            print(f" -- batch {batch}...")
            try:
                last_page = crawl_batches(subreddit, last_page, type="submission", start_utc=start_utc)
            except:
                time.sleep(3)
                continue
            submissions += last_page

            if batch % 10 == 0:
                # print(f" -- batch {batch}...")
                time.sleep(3)

            batch += 1

        if submissions != []:
            print(f"- Writing json file for year {y}...")
            with open(f"data/raw/submission-from-{orig_start}/{y}/subm_{subreddit}_{y}.json", "w") as json_file:
                json.dump(submissions, json_file)
        else: continue
    pass


def crawl_comments(subreddit, orig_start=2010, start_year=2010, end_year=2020):
    print(f"- Crawling comments after {start_year}...")

    for y in range(start_year, end_year):
        comments = []
        last_page = None
        batch = 1

        print(f" - year: {y}")
        start_utc = year2utc(y)

        while last_page != []:
            try:
                last_page = crawl_batches(subreddit, last_page, type="comment", start_utc=start_utc)
            except:
                time.sleep(3)
                continue
            comments += last_page

            if batch % 10 == 0:
                print(f" -- batch {batch}...")
                time.sleep(3)

            batch += 1

        if comments != []:
            print(f"- Writing json file for {y}...")
            with open(f"data/raw/comment-from-{orig_start}/{y}/comm_{subreddit}_{y}.json", 'w') as json_file:
                json.dump(comments, json_file)
        else: continue

    pass



def check_subreddit(subr, foldername):
    ## folder = "submission" or "comment"

    files = os.listdir(PATH + f"/data/raw/{foldername}")

    try: files.remove(".DS_Store")
    except: pass

    collected_subr = [f[5:-10] for f in files]
    if subr in collected_subr:
        result = True
    else:
        result = False
    return result


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--start_year", help="Crawling posts/comments posted after this date",
                           type=int, default=2010, required=False)
    argparser.add_argument("--end_year", help="Crawling posts/comments posted before this date",
                           type=int, default=2020, required=False)
    args = argparser.parse_args()
    orig_start_year = args.start_year
    start_year = orig_start_year
    end_year = args.end_year
    start_utc = year2utc(start_year)
    end_utc = year2utc(end_year)

    try: os.mkdir(PATH + "/data")
    except: pass
    try: os.mkdir(PATH + "/data/raw")
    except: pass
    try: os.mkdir(PATH + "/data/raw/comment-from-" + str(start_year))
    except: pass
    try: os.mkdir(PATH + "/data/raw/submission-from-" + str(start_year))
    except: pass

    for y in range(start_year, end_year):
        try: os.mkdir(PATH + f"/data/raw/comment-from-{start_year}/{y}")
        except: pass
        try: os.mkdir(PATH + f"/data/raw/submission-from-{start_year}/{y}")
        except: pass


    with open("data/left-right-labels.csv") as csvf:
        content = csvf.readlines()
    SUBREDDIT_LS = [elem.split(",")[0] for elem in content] # 101 subreddits
    SUBREDDIT_LS.pop(0)  # remove header


    CRAWLED = []
    for subr in SUBREDDIT_LS:
        print("subreddit:", subr)

        # crawl submissions
        print("Crawling submissions...")
        mark_year = None
        for y in range(end_year-1, start_year-1, -1):
            if check_subreddit(subr, f"submission-from-{start_year}/{y}") == True:
                mark_year = y
                break
        if mark_year:
            if mark_year == 2019:
                print(f"- Already crawled subreddit:", subr)
            else:
                print(f"- Resuming from year: {mark_year}")
                crawl_submissions(subr, orig_start=orig_start_year, start_year=mark_year+1, end_year=end_year)
        else:
            print(f"- Starting from year: {start_year}")
            crawl_submissions(subr, orig_start=orig_start_year, start_year=orig_start_year, end_year=end_year)

        # crawl comments
        print("Crawling comments...")
        mark_year = None
        for y in range(end_year-1, start_year-1, -1):
            if check_subreddit(subr, f"comment-from-{start_year}/{y}") == True:
                mark_year = y
                break
        if mark_year:
            if mark_year == 2019:
                print(f"- Already crawled subreddit:", subr)
            else:
                print(f"- Resuming from year: {mark_year}")
                crawl_comments(subr, orig_start=orig_start_year, start_year=mark_year+1, end_year=end_year)
        else:
            print(f"- Starting from year: {start_year}")
            crawl_comments(subr, orig_start=orig_start_year, start_year=orig_start_year, end_year=end_year)

        print(f"Finished crawling Subreddit {subr}!")
        # SUBREDDIT_LS.pop(0)


# code reference: https://www.textjuicer.com/2019/07/crawling-all-submissions-from-a-subreddit/

# python3 pipeline_reddit_fixstart_by_year.py --start_year=2016 --end_year=2021
