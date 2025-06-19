from flask import Flask, jsonify
from pymongo import MongoClient
import bcrypt, uuid
from datetime import datetime
from DB import db


if db is not None:
    users = db.users
else:
    users = None


class User:
    def createUser(self, email, password, user_type="client"):

        if self.checkUserPresent(email):
            return jsonify({"msg": "User is already Present", "success": False}), 400

        passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        token = str(uuid.uuid4())
        user = {
            "email": email,
            "password_hash": passwordHash,
            "user_type": user_type,
            "is_verified": False if user_type == "client" else True,
            "verification_token": token,
            "created_at": datetime.utcnow(),
        }

        users.insert_one(user)

        userObj = {
            "msg": "User Created Successfuly",
            "success": True,
            "token": token,
            "email": email,
            "userType": user_type,
        }
        return jsonify(userObj), 201


    def checkUserPresent(self, email):
        if users is None:
            return {"error": "Database connection failed"}, 500

        user = users.find_one({"email": email})
        if user:
            return True
        else:
            return False

    

userModel = User()
