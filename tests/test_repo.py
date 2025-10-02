import os
import pandas as pd
import pytest
from datetime import datetime, timedelta
from src.repo_miner import fetch_commits, fetch_issues

# --- Helpers for dummy GitHub API objects ---

class DummyAuthor:
    def __init__(self, name, email, date):
        self.name = name
        self.email = email
        self.date = date

class DummyCommitCommit:
    def __init__(self, author, message):
        self.author = author
        self.message = message

class DummyCommit:
    def __init__(self, sha, author, email, date, message):
        self.sha = sha
        self.commit = DummyCommitCommit(DummyAuthor(author, email, date), message)

class DummyUser:
    def __init__(self, login):
        self.login = login

class DummyIssue:
    def __init__(self, id_, number, title, user, state, created_at, closed_at, comments, is_pr=False):
        self.id = id_
        self.number = number
        self.title = title
        self.user = DummyUser(user)
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.comments = comments
        # attribute only on pull requests
        self.pull_request = DummyUser("pr") if is_pr else None

class DummyRepo:
    def __init__(self, commits, issues):
        self._commits = commits
        self._issues = issues

    def get_commits(self):
        return self._commits

    def get_issues(self, state="all"):
        if state == "all":
            return self._issues
        return [i for i in self._issues if i.state == state]

class DummyGithub:
    def __init__(self, token):
        assert token == "fake-token"
    def get_repo(self, repo_name):
        return self._repo

@pytest.fixture(autouse=True)
def patch_env_and_github(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    monkeypatch.setattr("src.repo_miner.Github", lambda token: gh_instance)

# Global placeholder
gh_instance = DummyGithub("fake-token")

# ------------------- Commit Tests -------------------

def test_fetch_commits_basic(monkeypatch):
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit\nDetails"),
        DummyCommit("sha2", "Bob", "b@example.com", now - timedelta(days=1), "Bug fix")
    ]
    gh_instance._repo = DummyRepo(commits, [])
    df = fetch_commits("any/repo")
    assert list(df.columns) == ["sha", "author", "email", "date", "message"]
    assert len(df) == 2
    assert df.iloc[0]["message"] == "Initial commit"

def test_fetch_commits_limit(monkeypatch):
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit"),
        DummyCommit("sha2", "Bob", "b@example.com", now, "Bug fix"),
    ]
    gh_instance._repo = DummyRepo(commits, [])
    df = fetch_commits("any/repo", max_commits=1)
    assert not df.empty
    assert len(df) == 1

def test_fetch_commits_empty(monkeypatch):
    gh_instance._repo = DummyRepo([], [])
    df = fetch_commits("any/repo")
    assert df.empty
    assert list(df.columns) == ["sha", "author", "email", "date", "message"]

def test_fetch_commits_message_content(monkeypatch):
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit with details"),
        DummyCommit("sha2", "Bob", "b@example.com", now, "Bug fix applied"),
    ]
    gh_instance._repo = DummyRepo(commits, [])
    df = fetch_commits("any/repo")
    assert len(df) == 2
    assert df.iloc[0]["message"] == "Initial commit with details"
    assert df.iloc[1]["message"] == "Bug fix applied"

def test_fetch_commits_date_format(monkeypatch):
    now = datetime.now()
    commits = [DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit")]
    gh_instance._repo = DummyRepo(commits, [])
    df = fetch_commits("any/repo")
    assert len(df) == 1
    assert "T" in df.iloc[0]["date"]

# ------------------- Issue Tests -------------------

def test_fetch_issues_basic(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Bug in login", "alice", "open", now, None, 5),
        DummyIssue(2, 102, "Fix typo", "bob", "closed", now - timedelta(days=2), now - timedelta(days=1), 2)
    ]
    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="all")
    assert not df.empty
    assert list(df.columns) == [
        "id", "number", "title", "user", "state",
        "created_at", "closed_at", "comments", "open_duration_days"
    ]
    assert len(df) == 2
    assert df.iloc[0]["title"] == "Bug in login"
    assert df.iloc[1]["state"] == "closed"

def test_fetch_issues_prs_excluded(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(3, 103, "PR should be skipped", "carol", "open", now, None, 1, is_pr=True),
        DummyIssue(4, 104, "Valid issue", "dave", "open", now, None, 0)
    ]
    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="all")
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Valid issue"

def test_fetch_issues_date_normalization(monkeypatch):
    now = datetime.now()
    issues = [DummyIssue(5, 105, "Check date", "eve", "open", now, None, 0)]
    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="all")
    assert len(df) == 1
    assert "T" in df.iloc[0]["created_at"]

def test_fetch_issues_open_duration(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(6, 106, "Closed issue", "frank", "closed", now - timedelta(days=5), now, 3)
    ]
    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="closed")
    assert len(df) == 1
    assert df.iloc[0]["open_duration_days"] == 5
