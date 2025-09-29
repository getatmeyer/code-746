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

    args = parser.parse_args()

    # Dispatch based on selected command
    if args.command == "fetch-commits":
        df = fetch_commits(args.repo, args.max_commits)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} commits to {args.out}")


if __name__ == "__main__":
    main()

