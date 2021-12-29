from os import write
from flask import Flask 
from flask import render_template 
from flask import request 
from pygal.style import LightColorizedStyle
from pygal.style import DarkColorizedStyle
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
        
@app.route("/gauges")
def gauges():
    try:
            
        username="Terlo"
        repo="Clothes-Annotation-Web-App"

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
        return render_template("radar.html",
                               graph_data = graph_data,
                               avatar=avatar,
                               contribs= contribs,
                               names=names,
                               len = len(names)                       
                               )
    except Exception as e:
        print("gauges page failed.")
        assert(False)
        


# @app.route("/radar")
# def radar_test():
#     try:
#         bar_chart = pygal.HorizontalBar()
#         bar_chart.title = 'Languages used'
#         for x in range(len(lan_list)):
#             bar_chart.add(lan_list[x][0],lan_list[x][1])
        
        
#         graph_data = bar_chart.render_data_uri() 
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