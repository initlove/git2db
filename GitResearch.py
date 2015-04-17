from git import Repo
from git import Commit
from git import Diff
import sys
import pymongo
from pymongo import MongoClient
from DMDatabase import DMDatabase
from bson.son import SON


def get_user_list(repo_name, db):
    result = db["git2db"].aggregate([
                       {"$group": {"_id": "$author", "count": {"$sum": 1}}}, 
                       {"$sort": SON([("count", -1), ("_id", -1)])}
                       ])
    print result

reload(sys)
sys.setdefaultencoding('utf-8')
db = DMDatabase().getDB()
repo_name = "gvfs"
get_user_list(repo_name, db)
