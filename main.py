from flask import Flask
import os
from dotenv import load_dotenv, dotenv_values


from DB import db_connection

load_dotenv()
app = Flask(__name__)


@app.route("/")
def hello():
    db_connection()
    return f"<p>{dbs} </p>"


"""
    # Routes
     - /Sign-up -> POST to server which checks database [userid, email, password]
     - /verify/<token> -> GET send a test mail to user to verify the identity
     - /Login -> POST to server and check database if user present or not [email, password]
     
     
     - /upload -> POST to server and upload the file in the database [fileName, fileID]
     - /download/:file_id -> GET to server and search for the file in database using file_id and dowload the file 
      
     - /uploads -> GET to server and return all the files available in the database. 

"""

app.run(debug=True)
