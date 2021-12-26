from os import write
from flask import Flask 
from flask import render_template 
from pygal.style import LightColorizedStyle
import pygal
import base64
import requests
from github import Github
from pprint import pprint
import json
from hidden import username 
from hidden import auth_token

app = Flask(__name__)
repo_list_names = ["a","b"]
repoValueTotal= []


#g = Github(auth_token)
g = Github()
user=g.get_user(username)

cumulative_languages_list = []
language_count=[]
languages_list=[]
total_languages = 0

#contains a tuple of languages and the amount of time the language occurs
#example [(python,3)(java,8)]
lan_list= []


def occurs(listval, item):
    count = 0
    for val in listval:
        if (val == item):
            count = count + 1
    return count

for x in user.get_repos():
    #print(f"repo name is: {x.name} the majority language is:{x.language}")
    #collect all of the languages that exist in the repositories.
    if x.language not in languages_list:
        languages_list.append(x.language)
        total_languages = total_languages+1     
    cumulative_languages_list.append(x.language)
    
    
    
    
for i in range(len(languages_list)):
    res = occurs(cumulative_languages_list,languages_list[i])
    print(f"{languages_list[i]} occurs in the list {res} amount of times")
    lan_list.append((languages_list[i],res))
    

print(f"{lan_list} \n")


print(total_languages)
print(f"{languages_list}\n")
        


# assert(False)
# for repo in user.get_repos():
#     the_user_total =0
#     contributions_count=0
#     the_user_total_contributions=0
    
    
#     repo_name = repo.name
#     repo_forks= repo.forks_count
#     repo_created_at = repo.created_at
#     # tst = repo.contributors_url
#     repo_commits = repo.commits_url
#     repo_merges = repo.merges_url
#     repo_watchers = repo.watchers_count
#     repo_commits = repo.get_commits
   
    
#     str_repo_names = str(repo_name)
#     repo_list_names.append(str_repo_names)
  
  
  
  
  
  
# values = requests.get(repo.contributors_url).json()
# for i in range(len(values)):
#     print(repo_name,values[i]['login'],values[i]['contributions'])
#     contributions_count=int(values[i]['contributions'])+contributions_count
#     cur_name =  str(values[i]['login'])
#     cur_name = cur_name.lower()
#     # print(f"The current username is->{cur_name}")
#     # print(f"The username is->{str(username).lower()}")
            
#     if cur_name == str(username).lower():
#         the_user_total_contributions= int(values[i]['contributions']) 
#         repoValueTotal.append((repo_name,[the_user_total_contributions,contributions_count]))
#     print(f"the total contributions to the repo is {contributions_count} \n")































# print(repo_list_names)

# print(repoValueTotal)
# print("clothes annotation web app==?  ",repoValueTotal[0][0])
# print("22==? ",repoValueTotal[0][1][0])
# print("232==? ",repoValueTotal[0][1][1])

@app.route("/")
def home():
    return render_template("index.html")
    

# @app.route("/gauges")
# def gauges():
#     try:
        
#         gauge = pygal.SolidGauge(inner_radius=0.70)
#         percent_formatter = lambda x: '{:.10g}%'.format(x)
#         dollar_formatter = lambda x: '{:.10g}$'.format(x)
#         gauge.value_formatter = percent_formatter
#         len_list = len(repoValueTotal)
#         for i in range(len_list):
#             print("called function.")
#             gauge.add(repoValueTotal[i][0], [{'value':repoValueTotal[i][1][0],'max_value':repoValueTotal[i][1][1]}])
#         gauge.render()
#         # radar_chart.render_in_browser()
#         graph_data = gauge.render_data_uri() 
#         return render_template("gauge.html", graph_data = graph_data)
#     except Exception as e:
#         assert(False)
        


# @app.route("/radar")
# def radar_test():
#     try:
#         radar_chart = pygal.Radar(style=LightColorizedStyle)
#         radar_chart.title = 'User Contributions'
#         radar_chart.x_labels = repo_list_names
#         radar_chart.add('mihoy minoy', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
#         radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
#         radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
#         radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
#         # radar_chart.render_in_browser()
#         graph_data = radar_chart.render_data_uri() 
#         return render_template("radar.html", graph_data = graph_data)
#     except Exception as e:
#         return (str(e))



# @app.route("/languages")
# def language_test():
#     try:
#         bar_chart = pygal.StackedBar()
#         bar_chart.title = 'Browser usage evolution (in %)'
#         bar_chart.x_labels = map(str, range(2002, 2013))
#         bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
#         bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
#         bar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
#         bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
#         bar_chart.render()
#         graph_data = bar_chart.render_data_uri() 
#         return render_template("languages.html", graph_data = graph_data)
#     except Exception as e:
#         return (str(e))
    
    
if __name__ == "__main__":
    app.run()