# Flask Github API data visualisation

This is a flask application to visualise data provided by the github API

## Getting Started
Clone the repo and navigate to the folder where the files are stored and open it in an IDE.

### Prerequisites
Python3
pip3

### Setting up a virtual environment.

To install a virtual environment. you might need to navigate to the scripts directory fot this command to work.
    
    C:\Users\<user name>\AppData\Local\Programs\Python\Python37\Scripts
    
    pip install virtualenv

Creating a virtual environment.

    Python3 -m <name of environment>  

Starting the virtual environment.

    <name of environment>\Scripts\activate.bat
   
Downloading the requirements.

    pip install -r /path/to/requirements.txt
    
 ### Running the Application
   
  To run the applicaion on localhost. In the working directory run: 
 
    py main.py
   
   In a web browser  type the following
   
    http://127.0.0.1:5000/
    
## What does this application do?
  Using the github API this applicaiton will allow you to 
     
  
   View the total number of commits per week to the repository for the last year.
  
  ![commits](https://user-images.githubusercontent.com/57776535/147995601-01042647-7c79-4a6b-b070-a8ffda5cada9.png)
  
      
   
   View a breakdown of contribitions to the repo by contributors.
  
   ![contributions](https://user-images.githubusercontent.com/57776535/147995139-78ae6932-ea28-434e-9936-af978635b950.png)

   
   
   
   View a breakdown of the ratio of additions to deletions of lines of code per user from all of their commits.
   
   ![ratio](https://user-images.githubusercontent.com/57776535/147995285-29147d4b-5a3a-4149-a41f-c7a7217a158b.png)
   
   
   
   View the prevalence of languages used in the repo
   
  ![langs](https://user-images.githubusercontent.com/57776535/147995802-406b83d8-5ebe-4fdf-9e0f-b3021a126489.png)

   
   View a list of all of the contributors to the repo.
  
  ![contributors](https://user-images.githubusercontent.com/57776535/147994968-5986d554-6576-4515-93c9-35579f6eeb58.png)



 
