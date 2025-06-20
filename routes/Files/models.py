from flask import Flask, jsonify
from DB import db



if db is not None:
    users = db.users
else:
    users = None


# class FileSys():
