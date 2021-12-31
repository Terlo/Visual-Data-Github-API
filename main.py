from os import write
from typing_extensions import Required
from flask import Flask 
from flask import render_template 
from flask import request
from pygal.graph.graph import Graph 
from pygal.style import LightColorizedStyle
from pygal.style import DarkColorizedStyle
import pygal
import base64
import requests
from github import Github
from pprint import pprint
import json
from traceback import print_exc, print_tb

# from requests.sessions import _Data
from hidden import username 
from hidden import auth_token

app = Flask(__name__)
repo_list_names = ["a","b"]
repoValueTotal= []


#g = Github(auth_token)
# g = Github()
# user=g.get_user(username)

cumulative_languages_list = []
language_count=[]
languages_list=[]
total_languages = 0

#contains a tuple of languages and the amount of time the language occurs
#example [(python,3)(java,8)]
lan_list= []


# def occurs(listval, item):
#     count = 0
#     for val in listval:
#         if (val == item):
#             count = count + 1
#     return count

# for x in user.get_repos():
#     #print(f"repo name is: {x.name} the majority language is:{x.language}")
#     #collect all of the languages that exist in the repositories.
#     if x.language not in languages_list:
#         languages_list.append(x.language)
#         total_languages = total_languages+1     
#     cumulative_languages_list.append(x.language)
    
# for i in range(len(languages_list)):
#     res = occurs(cumulative_languages_list,languages_list[i])
#     lan_list.append((languages_list[i],res))
# print(f"{lan_list} \n")


# print(total_languages)
# print(f"{languages_list}\n")
        



def occurs(listval, item):
    count = 0
    for val in listval:
        if (val == item):
            count = count + 1
    return count


@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    cumulative_languages_list = []
    lan_list=[]
    language_count=[]
    languages_list=[]
    total_languages = 0

    text = request.form['text']
    processed_text = text
    
    g = Github()
    user=g.get_user(processed_text)
    

    for x in user.get_repos():
    #print(f"repo name is: {x.name} the majority language is:{x.language}")
    #collect all of the languages that exist in the repositories.
        if x.language not in languages_list:
            languages_list.append(x.language)
            total_languages = total_languages+1     
        cumulative_languages_list.append(x.language)

    for i in range(len(languages_list)):
        res = occurs(cumulative_languages_list,languages_list[i])
        lan_list.append((languages_list[i],res))
        #print(f"{lan_list} \n")

       
       
    bar_chart = pygal.HorizontalBar()
    bar_chart.title = processed_text+'\'s Languages used'
    for x in range(len(lan_list)):
        bar_chart.add(lan_list[x][0],lan_list[x][1])


    graph_data = bar_chart.render_data_uri() 
    return render_template("radar.html",graph_data=graph_data)



def contributorsURL(username, repo):
    link =  "https://api.github.com/repos/"+username+"/"+repo+"/contributors"
    return link

@app.route('/repo')
def my_formz():
    return render_template('index.html')

@app.route("/repo",methods=['POST'])
def gauges():
    r_name,r_additions,r_deletions,perc_deletions,perc_additions,r_commits =[],[],[],[],[],[]
    try:
         
        username = request.form['username']    
        repo = request.form['repository']    
        # username="Terlo"
        # repo="Clothes-Annotation-Web-App"

        link = contributorsURL(username,repo)
        data  = requests.get(link).json()
        pprint(data)  

        avatar,names,contribs= [], [], []
        for collection in data:
            names.append(collection['login'])
            contribs.append(collection['contributions'])
            avatar.append(collection['avatar_url'])
            
        total_contributions = sum(contribs)
        
        
        pie_chart = pygal.Pie(inner_radius=.75, style=DarkColorizedStyle)
        pie_chart.title = 'Contributions to '+ repo+ ' by users.'

        for i in range(len(names)):
            pie_chart.add(names[i], contribs[i])



        graph_data = pie_chart.render_data_uri() 
        
        #g = Github(auth_token)
        g = Github()
        user=g.get_user(username)
        repositories = user.get_repos()
        repoName = repo
        for x in repositories:
            if repoName in x.name:
                required_repo = x
                # pprint(f"\n weekly commit statistics1 ->\n{x.get_stats_participation().all}")
                print("\n\n------------------------------------------------------------------------")
                the_data  = required_repo.get_stats_contributors()
                
                for i in range(len(the_data)):
                    addition_count =0
                    deletion_count =0
                    commit_count =0
                    
                    for j in range(len(the_data[i].raw_data['weeks'])):
                    # print(f"\n the author{the_data[i].author}")
                    # pprint(f"additions: {the_data[i].raw_data['weeks'][j]['a']} ")
                    # pprint(f"deletions: {the_data[i].raw_data['weeks'][j]['d']} ")
                    # pprint(f"contributions: {the_data[i].raw_data['weeks'][j]['c']} ")
                        
                        addition_count = the_data[i].raw_data['weeks'][j]['a'] +addition_count
                        deletion_count = the_data[i].raw_data['weeks'][j]['d'] +deletion_count
                        commit_count = the_data[i].raw_data['weeks'][j]['c'] +commit_count
                        
                    print(f"{the_data[i].author} has a total of {addition_count} additions, {deletion_count}, deletions {commit_count}, commits")
                    r_name.append(the_data[i].author.login)
                    r_additions.append(addition_count)
                    r_deletions.append(deletion_count)
                    r_commits.append(commit_count)
                    a = ((addition_count)/((addition_count)+(deletion_count)))
                    b = ((deletion_count)/((addition_count)+(deletion_count)))
                    
                    _a = a*100
                    _b = b*100
                    
                    # print(f"_a :{_a}")
                    # print(f"_b :{_b}")
                    perc_additions.append(_a)
                    perc_deletions.append(_b)
                    
                    
                    print(perc_additions)
                    print(perc_deletions)
                                        
                for i in range(len(r_name)):  
                    print(r_name[i],r_additions[i],r_deletions[i],r_commits[i])
                radar_chart = pygal.Radar( style=DarkColorizedStyle)
                radar_chart.title = 'ratio of addition:deleltion of lines of code per commit'
                radar_chart.x_labels =r_name
                
                
                #radar_chart.add("code commits", r_commits)
                radar_chart.add("code additions(%)", perc_additions)
                radar_chart.add("code deletions(%)", perc_deletions)
                radar_chart.render()        
            break      
        graph_data1 = radar_chart.render_data_uri()
        print("made it here lol") 
        
        #username = "terlo"
        #g = Github(auth_token)
        g = Github()
        user=g.get_user(username)

        #once = False
        repositories = user.get_repos()
        #repoName = "Clothes-Annotation-Web-App"
        y_values = []
        for x in repositories:
            if repoName in x.name:
                #print("found the repo :DDDDDD")
                y_values = x.get_stats_participation().all
                print(y_values)
        #bar_chart = pygal.HorizontalBar()
        line_chart = pygal.StackedLine(fill=True, style=DarkColorizedStyle)
        line_chart.title = 'commits lol'
        line_chart.x_labels = map(str, range(52))
        line_chart.add('commits', y_values)

        graph_data2 = line_chart.render_data_uri() 
        
        return render_template("radar.html",
                               graph_data = graph_data,
                               graph_data1 = graph_data1,
                               graph_data2 = graph_data2,
                               avatar=avatar,
                               contribs= contribs,
                               names=names,
                               lenlist = len(names)                       
                               )
    except Exception as e:
        print("gauges page failed.")
        assert(False)
        


@app.route("/w")
def radar_test():
    try:
        
        username = "terlo"
        #g = Github(auth_token)
        g = Github()
        user=g.get_user(username)

        once = False
        repositories = user.get_repos()
        repoName = "Clothes-Annotation-Web-App"
        y_values = []
        for x in repositories:
            if repoName in x.name:
                print("found the repo :DDDDDD")
                y_values = x.get_stats_participation().all
                print(y_values)
        #bar_chart = pygal.HorizontalBar()
        line_chart = pygal.StackedLine(fill=True, style=DarkColorizedStyle)
        line_chart.title = 'commits lol'
        line_chart.x_labels = map(str, range(52))
        line_chart.add('commits', y_values)

        line_chart.render()
        graph_data = line_chart.render_data_uri() 
        return render_template("languages.html", graph_data = graph_data)
    except Exception as e:
        return (str(e))

@app.route("/a")
def radar():
    r_name,r_additions,r_deletions,perc_deletions,perc_additions,r_commits =[],[],[],[],[],[]
    try:
        
        username = "terlo"
        repoName = "Clothes-Annotation-Web-App"
        #g = Github(auth_token)
        g = Github()
        user=g.get_user(username)
        repositories = user.get_repos()

        for x in repositories:
            if repoName in x.name:
                required_repo = x
                # pprint(f"\n weekly commit statistics1 ->\n{x.get_stats_participation().all}")
                print("\n\n------------------------------------------------------------------------")
                the_data  = required_repo.get_stats_contributors()
                
                for i in range(len(the_data)):
                    addition_count =0
                    deletion_count =0
                    commit_count =0
                    
                    for j in range(len(the_data[i].raw_data['weeks'])):
                    # print(f"\n the author{the_data[i].author}")
                    # pprint(f"additions: {the_data[i].raw_data['weeks'][j]['a']} ")
                    # pprint(f"deletions: {the_data[i].raw_data['weeks'][j]['d']} ")
                    # pprint(f"contributions: {the_data[i].raw_data['weeks'][j]['c']} ")
                        
                        addition_count = the_data[i].raw_data['weeks'][j]['a'] +addition_count
                        deletion_count = the_data[i].raw_data['weeks'][j]['d'] +deletion_count
                        commit_count = the_data[i].raw_data['weeks'][j]['c'] +commit_count
                        
                    print(f"{the_data[i].author} has a total of {addition_count} additions, {deletion_count}, deletions {commit_count}, commits")
                    r_name.append(the_data[i].author.login)
                    r_additions.append(addition_count)
                    r_deletions.append(deletion_count)
                    r_commits.append(commit_count)
                    a = ((addition_count)/((addition_count)+(deletion_count)))
                    b = ((deletion_count)/((addition_count)+(deletion_count)))
                    
                    _a = a*100
                    _b = b*100
                    
                    # print(f"_a :{_a}")
                    # print(f"_b :{_b}")
                    perc_additions.append(_a)
                    perc_deletions.append(_b)
                    
                    
                    print(perc_additions)
                    print(perc_deletions)
                                        
                for i in range(len(r_name)):  
                    print(r_name[i],r_additions[i],r_deletions[i],r_commits[i])
                radar_chart = pygal.Radar( style=DarkColorizedStyle)
                radar_chart.title = 'ratio of addition:deleltion of lines of code per commit'
                radar_chart.x_labels =r_name
                
                
                radar_chart.add("code commits", r_commits)
                radar_chart.add("code additions(%)", perc_additions)
                radar_chart.add("code deletions(%)", perc_deletions)
                radar_chart.render()        
            break      
        graph_data = radar_chart.render_data_uri()
        print("made it here lol") 
        return render_template("languages.html", graph_data = graph_data)
    except Exception as e:
            return "print_exc()"



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