# import os
# import argparse
# import pandas as pd
# from github import Github

# def fetch_commits(repo_full_name: str, max_commits: int = None) -> pd.DataFrame:
#     """
#     Fetch commits from a GitHub repository into a DataFrame.
#     Columns: sha, author, email, date (ISO-8601), message (first line only).
#     """

# # 1. Read GitHub token from environment variable 
# github_token = os.getenv("GITHUB_TOKEN")


# # Initialize GitHub client
# g = Github(github_token)


# # 2. Get a repository (format: "owner/repo_name")
# repo_name = "getatmeyer/code-746"
# repo = g.get_repo(repo_name)

# # 3. Fetch commits (paginated automatically by PyGithub)
# commits = repo.get_commits()  # returns a PaginatedList

# # 4. Normalize each commit into a dictionary
# commit_records = []

# # 5. Normalize commits
# commit_records = []
# count = 0
# for commit in commits:
#         record = {
#             "sha": commit.sha,
#             "author": commit.commit.author.name if commit.commit.author else None,
#             "email": commit.commit.author.email if commit.commit.author else None,
#             "date": commit.commit.author.date.isoformat() if commit.commit.author else None,
#             "message": commit.commit.message.splitlines()[0] if commit.commit.message else None
           
#         }
#         commit_records.append(record)

#         count += 1
#         if max_commits and count >= max_commits:
#             break
        
#         return pd.DataFrame(commit_records)

    

# def main():
#     """
#     Parse command-line arguments and dispatch to sub-commands.
#     """
#     parser = argparse.ArgumentParser(
#         prog="repo_miner",
#         description="Fetch GitHub commits/issues and summarize them"
#     )
#     subparsers = parser.add_subparsers(dest="command", required=True)

#     # Sub-command: fetch-commits
#     c1 = subparsers.add_parser("fetch-commits", help="Fetch commits and save to CSV")
#     c1.add_argument("--repo", required=True, help="Repository in owner/repo format")
#     c1.add_argument("--max",  type=int, dest="max_commits",
#                     help="Max number of commits to fetch")
#     c1.add_argument("--out",  required=True, help="Path to output commits CSV")

#     args = parser.parse_args()

#     # Dispatch based on selected command
#     if args.command == "fetch-commits":
#         df = fetch_commits(args.repo, args.max_commits)
#         df.to_csv(args.out, index=False)
#         print(f"Saved {len(df)} commits to {args.out}")

# if __name__ == "__main__":
#     main()
# import os
# import argparse
# import pandas as pd
# from github import Github

# def fetch_commits(repo_full_name: str, max_commits: int = None) -> pd.DataFrame:
#     """
#     Fetch commits from a GitHub repository into a DataFrame.
#     Columns: sha, author, email, date (ISO-8601), message (first line only).
#     """
#     # 1. Read GitHub token from environment variable
#     github_token = os.getenv("GITHUB_TOKEN")
#     if not github_token:
#         raise ValueError("GITHUB_TOKEN environment variable not set.")

#     # 2. Initialize GitHub client
#     g = Github(github_token)

#     # 3. Get repository
#     repo = g.get_repo(repo_full_name)

#     # 4. Fetch commits (paginated)
#     commits = repo.get_commits()
#     commit_records = []

#     # 5. Normalize commits
#     count = 0
#     for commit in commits:
#         author = commit.commit.author
#         record = {
#             "sha": commit.sha,
#             "author": author.name if author else None,
#             "email": author.email if author else None,
#             "date": author.date.isoformat() if author else None,
#             "message": commit.commit.message.splitlines()[0] if commit.commit.message else None
#         }
#         commit_records.append(record)
#         count += 1
#         if max_commits and count >= max_commits:
#             break

#     # 6. Return as DataFrame
#     return pd.DataFrame(commit_records)


# def main():
#     """
#     Parse command-line arguments and dispatch to sub-commands.
#     """
#     parser = argparse.ArgumentParser(
#         prog="repo_miner",
#         description="Fetch GitHub commits/issues and summarize them"
#     )
#     subparsers = parser.add_subparsers(dest="command", required=True)

#     # Sub-command: fetch-commits
#     c1 = subparsers.add_parser("fetch-commits", help="Fetch commits and save to CSV")
#     c1.add_argument("--repo", required=True, help="Repository in owner/repo format")
#     c1.add_argument("--max",  type=int, dest="max_commits",
#                     help="Max number of commits to fetch")
#     c1.add_argument("--out",  required=True, help="Path to output commits CSV")

#     args = parser.parse_args()

#     # Dispatch based on selected command
#     if args.command == "fetch-commits":
#         df = fetch_commits(args.repo, args.max_commits)
#         df.to_csv(args.out, index=False)
#         print(f"Saved {len(df)} commits to {args.out}")


# if __name__ == "__main__":
#     main()
import os
import argparse
import pandas as pd
from github import Github

def fetch_commits(repo_full_name: str, max_commits: int = None) -> pd.DataFrame:
    """
    Fetch commits from a GitHub repository into a DataFrame.
    Columns: sha, author, email, date (ISO-8601), message (first line only).
    """
    # 1. Read GitHub token from environment variable
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    # 2. Initialize GitHub client
    g = Github(github_token)

    # 3. Get repository
    repo = g.get_repo(repo_full_name)

    # 4. Fetch commits (paginated)
    commits = repo.get_commits()
    commit_records = []

# 5. Normalize commits
    count = 0
    for commit in commits:
        author = commit.commit.author
        record = {
            "sha": commit.sha,
            "author": author.name if author else None,
            "email": author.email if author else None,
            "date": author.date.isoformat() if author else None,
            "message": commit.commit.message.splitlines()[0] if commit.commit.message else None
        }
        commit_records.append(record)
        count += 1
        if max_commits and count >= max_commits:
            break

# 6. Return as DataFrame (even if empty, ensure consistent columns)
    if not commit_records:
        return pd.DataFrame(columns=["sha", "author", "email", "date", "message"])
    return pd.DataFrame(commit_records)

#. <<< fetch_issues
def fetch_issues(repo_full_name: str, state: str = "all", max_issues: int = None) -> pd.DataFrame:
    """
    Fetch issues from a GitHub repository into a DataFrame.
    Columns: id, number, title, user, state, created_at, closed_at, comments, open_duration_days
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    g = Github(github_token)
    repo = g.get_repo(repo_full_name)

    issues = repo.get_issues(state=state)
    issue_records = []

    count = 0
    for issue in issues:
        
        # Skip pull requests (they also show up in issues)
        if hasattr(issue, "pull_request") and issue.pull_request is not None:
            continue

        record = {
            "id": issue.id,
            "number": issue.number,
            "title": issue.title,
            "user": issue.user.login if issue.user else None,
            "state": issue.state,
            "created_at": issue.created_at.isoformat() if issue.created_at else None,
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "comments": issue.comments,
            "open_duration_days": (
                (issue.closed_at - issue.created_at).days
                if issue.closed_at and issue.created_at else None
            )
        }
        issue_records.append(record)

        count += 1
        if max_issues and count >= max_issues:
            break

    if not issue_records:
        return pd.DataFrame(columns=[
            "id", "number", "title", "user", "state",
            "created_at", "closed_at", "comments", "open_duration_days"
        ])
    return pd.DataFrame(issue_records)

def merge_and_summarize(commits_df: pd.DataFrame, issues_df: pd.DataFrame) -> None:
    """
    Merge-by-time and print:
      • Top 5 committers by count
      • Issue close rate (closed / total)
      • Average open duration (days) for closed issues
      • A small daily activity table (commits vs issues opened)
    """

# Copy so we don't mutate caller's DataFrames
    commits = commits_df.copy()
    issues  = issues_df.copy()

# --- Normalize timestamps to real datetimes ---
    commits['date']      = pd.to_datetime(commits.get('date'), errors='coerce', utc=True)
    issues['created_at'] = pd.to_datetime(issues.get('created_at'), errors='coerce', utc=True)
    issues['closed_at']  = pd.to_datetime(issues.get('closed_at'), errors='coerce', utc=True)

# --- 1) Top 5 committers ---
    print("\nTop 5 Committers:")
    if 'author' in commits.columns and not commits.empty:
        top_committers = commits['author'].fillna('Unknown').value_counts().head(5)
        print(top_committers.to_string())
    else:
        print("(no commit data)")

# --- 2) Issue close rate ---
    print("\nIssue Close Rate:")
    if not issues.empty and 'state' in issues.columns:
        states = issues['state'].astype(str).str.lower()
        total_issues  = len(states)
        closed_issues = (states == 'closed').sum()
        close_rate    = (closed_issues / total_issues * 100) if total_issues else 0.0
        # print(f"{closed_issues}/{total_issues} = {close_rate:.2f}%")
        print(f"Issue close rate ({closed_issues}/{total_issues}): {closed_issues/total_issues:.2f}")

    else:
        print("(no issue data)")

# --- 3) Average open duration (days) for closed issues ---
    print("\nAverage Open Duration (closed issues):")
    if {'created_at', 'closed_at'}.issubset(issues.columns):
        closed_only = issues.dropna(subset=['created_at', 'closed_at'])
        if not closed_only.empty:
            durations = (closed_only['closed_at'] - closed_only['created_at']).dt.days
            print(f"{durations.mean():.2f} days")
        else:
            print("(no closed issues with both dates)")
    else:
        print("(missing created_at/closed_at columns)")




def main():
    """
    Parse command-line arguments and dispatch to sub-commands.
    """
    parser = argparse.ArgumentParser(
        prog="repo_miner",
        description="Fetch GitHub commits/issues and summarize them"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-command: fetch-commits
    c1 = subparsers.add_parser("fetch-commits", help="Fetch commits and save to CSV")
    c1.add_argument("--repo", required=True, help="Repository in owner/repo format")
    c1.add_argument("--max",  type=int, dest="max_commits",
                    help="Max number of commits to fetch")
    c1.add_argument("--out",  required=True, help="Path to output commits CSV")

    # Sub-command: fetch-issues
    c2 = subparsers.add_parser("fetch-issues", help="Fetch issues and save to CSV")
    c2.add_argument("--repo", required=True, help="Repository in owner/repo format")
    c2.add_argument("--state", choices=["all", "open", "closed"], default="all",
                    help="Which issues to fetch")
    c2.add_argument("--max", type=int, dest="max_issues",
                    help="Max number of issues to fetch")
    c2.add_argument("--out", required=True, help="Path to output issues CSV")

    # << ADD: summarize subcommand >>
    c3 = subparsers.add_parser("summarize", help="Summarize commits and issues")
    c3.add_argument("--commits", required=True, help="Path to commits CSV (from fetch-commits)")
    c3.add_argument("--issues",  required=True, help="Path to issues CSV (from fetch-issues)")

    args = parser.parse_args()

# <<<Dispatch based on fetch-commits  >>> ------------------------------------------
    if args.command == "fetch-commits":
        df = fetch_commits(args.repo, args.max_commits)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} commits to {args.out}")
# <<< END

# <<< Dispatcher based on fetch-issues >>> ------------------------------------------
    if args.command == "fetch-issues":
        df = fetch_issues(args.repo, args.state, args.max_issues)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} issues to {args.out}")
# <<< END

# <<< Dispatcher based on summarize >>> ------------------------------------------
    if args.command == "summarize":
        # Read CSVs into DataFrames
        commits_df = pd.read_csv(args.commits)
        issues_df  = pd.read_csv(args.issues)
        # Generate and print the summary
        merge_and_summarize(commits_df, issues_df)
# <<< END

if __name__ == "__main__":
    main()


