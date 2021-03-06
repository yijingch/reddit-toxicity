# Toxicity at scale?
A structural view of conversation quality in political subreddits

Class project repository:
- DNDS 6014: Introduction to Computational Social Science
- DNDS 6291: Statistical Methods in Network Science

## Research questions

**Overarching RQ:** Where and how do toxic conversations happen online?

(A) User-level:
- A1: Who talks toxically?
- A2.1: Are my neighbors generally more toxic than me (i.e., toxicity friendship paradox)?
- A2.2: Does the TFP (if any) persist over time?

(B) Submission-level:
- B1: How do toxic conversations usually structure?
- B2: How do toxic conversations unfold?

## Code guide
- `pipeline-reddit-fixstart-by-year.py`: crawl Reddit submissions and comments through Pushshift API
- `parse-to-db.py`: parse .json files to sqlite .db
- `select-user.py`: write lists of active users for future subsetting in analysis
- `basic-descriptives.ipynb`: produce basic descriptives of the entire dataset
- `user-level-static.ipynb`: answers A1 and A2.1
- `user-level-tfp-overtime.ipynb`: answers A2.2
- `subm-level.ipynb`: answers B1 and B2
- `utils.py`: basic utility functions such as importing data and building networks

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
[1] Eom, Y. H., & Jo, H. H. (2014). Generalized friendship paradox in complex networks: The case of scientific collaboration. Scientific reports, 4(1), 1-6.

[2] Goel, S., Anderson, A., Hofman, J., & Watts, D. J. (2016). The structural virality of online diffusion. Management Science, 62(1), 180-196.

[3] Rajadesingan, A., Resnick, P., & Budak, C. (2020, May). Quick, community-specific learning: How distinctive toxicity norms are maintained in political subreddits. In Proceedings of the International AAAI Conference on Web and Social Media (Vol. 14, pp. 557-568).
