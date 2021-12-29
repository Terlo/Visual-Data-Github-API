from pygal.style import LightColorizedStyle
import pygal
import base64
import requests
from github import Github
from pprint import pprint
import json
from hidden import username 
from hidden import auth_token

repo_list_names = ["a","b"]
repoValueTotal= []

username = "terlo"
#g = Github(auth_token)
g = Github()
user=g.get_user(username)

once = False
repositories = user.get_repos()



username="Terlo"
repo="Clothes-Annotation-Web-App"

def contributorsURL(username, repo):
  link =  "https://api.github.com/repos/"+username+"/"+repo+"/contributors"
  return link
    

link = contributorsURL(username,repo)
data  = requests.get(link).json()
pprint(data)

avatar,names,contribs= [], [], []
for collection in data:
    names.append(collection['login'])
    contribs.append(collection['contributions'])
    avatar.append(collection['avatar_url'])
    
total_contributions = sum(contribs)



print(names)
print(avatar)
print(contribs)

# commits= requests.get(commits_json).json()
# contribs= requests.get(contributors_json).json()
# merges= requests.get(merges_json).json()

# pprint(f"\ncommits :\n {commits}")
# pprint(f"\ncontributions : \n{contribs}")
# pprint(f"\nmerges : \n{merges}")