# Toxicity at scale?
A structural view of conversation quality in political subreddits

Class project repository:
- DNDS 6014: Introduction to Computational Social Science
- DNDS 6291: Statistical Methods in Network Science

## Research questions

**Overarching RQ:** Where and how do toxic conversations happen online?

(A) User-level:
- A1: Who talks toxically?
- A2.1: Are my neighbors generally more toxic than me?
- A2.2: Does the paradox (if any) persist over time?

(B) Thread-level:
- B1: How do toxic conversations usually structure?
- B2: How do toxic conversations unfold?

## Code guide
- `pipeline_reddit_fixstart_by_year.py`: crawl Reddit submissions and comments through Pushshift API
- `parse_to_db.py`: parse .json files to sqlite .db
- `select-user.py`: write lists of active users for future subsetting in analysis
- `basic-descriptives.ipynb`: produce basic descriptives of the entire dataset
- ``

## Dataset
User-generated content retrieved from 51 active political subreddits from Jan 2012 to Dec 2015.
- 1.4m+ submissions
- 20m+ comments
- 900k+ unique users

**Ethics and privacy concerns of dataset collection/management**:
- Collected through Pushshift API
- Analyzed/discussed only in the academic setting
- Personally identifiable information is either aggregated or anonymized.
- Raw data or text content will not be released here.

## Reference

[1] Goel, S., Anderson, A., Hofman, J., & Watts, D. J. (2016). The structural virality of online diffusion. Management Science, 62(1), 180-196.

[2] Foti, N. J., Hughes, J. M., & Rockmore, D. N. (2011). Nonparametric sparsification of complex multiscale networks. PloS one, 6(2), e16431.
