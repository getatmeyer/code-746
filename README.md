# SWEN-746 Project

## Structure
- `src/` – source code
- `venv/` – Python virtual environment
- `requirements.txt` – Python dependencies

## Setup

1. Create and activate a virtual enviorment
- `bash` - source venv/bin/activate

"""
repo_miner.py — Homework 5
Fetch GitHub commits/issues and summarize key repository activity.
Author: Nathan Meyer
"""

### Homework 5 – Summarize Function

This homework adds a new command called summarize to repo_miner.py.
It combines data from commits and issues, then prints out important repo stats like the top committers, how many issues are closed, and how long issues stay open.

#### Usage
run terminal

python -m src.repo_miner fetch-commits --repo octocat/Hello-World --max 50 --out data/commits.csv

python -m src.repo_miner fetch-issues  --repo octocat/Hello-World --state closed --max 50 --out data/issues.csv

python -m src.repo_miner summarize --commits data/commits.csv --issues data/issues.csv


#### Results
Top 5 Committers:
The Octocat                1
Johnneylee Jack Rollins    1
cameronmcefee              1

Issue Close Rate (2/3): 0.67
Average Open Duration (closed issues): 2.32 days

