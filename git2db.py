from git import Repo
from git import Commit
from git import Diff

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
        
def get_commits (url):
    repo = Repo("/tmp/test/gvfs")
    commits = list(repo.iter_commits('master'))
    commits_len = len(commits)
    for i in range(0, commits_len-1):
        commit_cur = commits[i]
        commit_prev = commits[i+1]
        diff_str = repo.git.diff(commit_cur, commit_prev)
        (minus, plus) = get_diff_meta(diff_str)
        commit_data = {"sha": str(commit_cur),
                       "author": commit_cur.author.name, "email": commit_cur.author.email, 
                       "message": commit_cur.message, 
                       "minus": minus, "plus": plus}
        print commit_data
    #FIXME: how about the first one?

url = "/tmp/text/gvfs"
get_commits(url)
