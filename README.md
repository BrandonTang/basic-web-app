# Basic-Web-App
Basic-Web-App is a web application built under a backend Flask framework and frontend Bootstrap framework.

The purpose of this application is to allow users to create user accounts and upload files with captions after being logged in. Users can then delete their own submissions, or edit the captions of their submissions. This application was created for an Application Security course.

## Setup Instructions
Clone the git repository:

    git clone https://github.com/BrandonTang/basic-web-app.git

Create a virtual environment and install the requirements:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Install sqlite3 by following instructions at the following site:

    https://www.tutorialspoint.com/sqlite/sqlite_installation.htm
    
Initialize the database by entering the following in the command line:

    sqlite3 appsec.db < schema.sql
    
Locally run the application by entering the following in the command line:

    python main.py
