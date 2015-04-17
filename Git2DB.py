from git import Repo
from git import Commit
from git import Diff
import sys
import os
import pymongo
from pymongo import MongoClient
from DMDatabase import DMDatabase

def get_diff_meta(diff_str):
    lines = diff_str.split('\n')
    minus = 0
    plus = 0
    for line in lines:
        if line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("-"):
            minus += 1
        elif line.startswith("+"):
            plus += 1
    return  (minus, plus)

def get_repo_url(repo_name):
    url = os.path.join("/tmp/test", repo_name);
    return url

#    commit
#    __slots__ = ("tree",
#                 "author", "authored_date", "author_tz_offset",
#                 "committer", "committed_date", "committer_tz_offset",
#                 "message", "parents", "encoding", "gpgsig")

def get_commits(repo_name, db):
    url = get_repo_url(repo_name)
    repo = Repo(url)
    commits = list(repo.iter_commits('master'))
    commits_len = len(commits)
    for i in range(0, commits_len-1):
        commit_cur = commits[i]
        commit_prev = commits[i+1]
        minus = 1
        plus = 1
        try:
            diff_str = repo.git.diff(commit_cur, commit_prev)
        except Exception:
            print "exception in encode utf8"
            
        else:
            (minus, plus) = get_diff_meta(diff_str)
        commit_data = {"uniq": repo_name + '/' + str(commit_cur),
                       "repo_name": repo_name,
                       "sha": str(commit_cur),
                       "author": commit_cur.author.name,
                       "email": commit_cur.author.email,
                       "authored_date": commit_cur.authored_date,
                       "committed_date": commit_cur.committed_date,
                       "message": commit_cur.message, 
                       "encoding": commit_cur.encoding,
                       "minus": minus, "plus": plus}
        if db["git2db"].find_one({"uniq": repo_name + '/' + str(commit_cur)}):
            continue
        else:
            db["git2db"].insert(commit_data)
    #FIXME: how about the first one?

reload(sys)
sys.setdefaultencoding('utf-8')
db = DMDatabase().getDB()
repo_name = "gvfs"
get_commits(repo_name, db)
