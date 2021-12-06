# Toxicity at scale?
A structural view of conversation quality in political subreddits

Class project repository:
- DNDS 6014: Introduction to Computational Social Science
- DNDS 6291: Statistical Methods in Network Science

## Research questions


### code guide
- `pipeline_reddit_fixstart_by_year.py`: crawl Reddit submissions and comments through Pushshift API
- `parse_to_db.py`: parse .json files to sqlite .db
- `basic-descriptives.ipynb`: produce basic descriptives of the entire dataset
- ``

### data and index

- userlist:
  - `indx/ACTIVEUSERS_ALLYEARS2_10.csv`: users who have posted more than or equal to 10 times in at least 2 submissions from 2012 to 2015.
  - `indx/ACTIVEUSERS_ALLYEARS2_20.csv`: users who have posted more than or equal to 20 times in at least 2 submissions from 2012 to 2015.
  - `indx/ACTIVEUSERS_ALLYEARS2_50.csv`: users who have posted more than or equal to 50 times in at least 2 submissions from 2012 to 2015.
  - `indx/ACTIVEUSERS_ALLYEARS2_50.csv`: users who have posted more than or equal to 100 times in at least 5 submissions from 2012 to 2015 (a very small subset for pipeline debugging)
