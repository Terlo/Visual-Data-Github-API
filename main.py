import base64
import pygal
import requests
from github import Github
from pprint import pprint
import json




username = ""
auth_token = ""

g = Github(auth_token)
user=g.get_user(username)
for repo in user.get_repos():
    repo_name = repo.name
    repo_forks= repo.forks_count
    repo_created_at = repo.created_at
    tst = repo.contributors_url
    
    print(f"{repo_name}")
    r = requests.get(tst)
    v = r.json()
    print(v)
    print(v[0]['login'],v[0]['contributions'])
    print("\n\n\n\n")
    



