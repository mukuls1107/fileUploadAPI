from flask import Flask, jsonify
from pymongo import MongoClient
import bcrypt, uuid
from datetime import datetime, timedelta
from DB import db


from utility.email_util import sendMail

if db is not None:
    users = db.users
else:
    users = None


class User:

    def getUserInfo(self, email):
        if users is None:
            return {"error": "Database connection failed"}, 500

        user = users.find_one({"email": email})

        if user:
            return user
        else:
            return None

    def getUserAccessToken(self, token):
        if users is None:
            return {"error": "Database connection failed"}, 500

        user = users.find_one({"access_token.value": token})

        if user:
            tokenData = user.get("access_token")
            if tokenData and datetime.utcnow() < tokenData["expires_at"]:

                return tokenData
        else:
            users.update_one({"_id": user["_id"]}, {"$unset": {"access_token": ""}})
            return False

    def addTokeninUser(self, email, token):
        users.find_one_and_update(
            {"email": email},
            {
                "$set": {
                    "access_token": {
                        "value": token,
                        "expires_at": datetime.utcnow() + timedelta(minutes=5),
                    }
                }
            },
        )

    def createUser(self, email, password, userType="client"):

        passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        token = str(uuid.uuid4())
        user = {
            "email": email,
            "passwordHash": passwordHash,
            "userType": userType,
            "isVerified": False if userType.lower() == "client" else True,
            "verificationToken": token,
            "createdAt": datetime.utcnow(),
        }

        users.insert_one(user)

        userObj = {
            "msg": "User Created Successfuly",
            "success": True,
            "token": token,
            "email": email,
            "userType": userType,
        }
        # "link": f"http://localhost:5000/api/users/verify/{token}"
        if userObj["userType"] == "client":
            sendMail(userObj["email"], userObj["token"], "Verification Link")

        return jsonify(userObj), 201

    def checkUserPresent(self, email):
        if users is None:
            return {"error": "Database connection failed"}, 500

        user = users.find_one({"email": email})
        if user:
            return True
        else:
            return False

    def verifyEmail(self, token):
        if users is None:
            return jsonify({"msg": "db connection failed", "success": False}), 500

        user = users.find_one({"verificationToken": token})

        if not user:
            return jsonify({"msg": "Invalid token", "success": False}), 404

        if user["isVerified"] == True:
            return jsonify({"msg": "User is already verified", "success": True}), 200

        timeSinceTokenGenerated = datetime.utcnow() - user["createdAt"]
        if timeSinceTokenGenerated > timedelta(minutes=2):
            self.resendVerification(user["email"])
            return (
                jsonify(
                    {
                        "success": False,
                        "msg": "A new verification link has been sent on the mail.",
                    }
                ),
                410,
            )

        users.update_one({"_id": user["_id"]}, {"$set": {"isVerified": True}})

        return (
            jsonify(
                {
                    "msg": "User Verification successfull",
                    "success": True,
                }
            ),
            200,
        )

    def resendVerification(self, email):
        user = users.find_one({"email": email})

        if not user:
            return (
                jsonify(
                    {
                        "msg": "User not found",
                        "success": False,
                    }
                ),
                404,
            )

        if user["isVerified"] == True:
            return jsonify({"msg": "User is already verified", "success": True}), 200

        newToken = str(uuid.uuid4())

        users.update_one(
            {"_id": user["_id"]},
            {"$set": {"verificationToken": newToken, "createdAt": datetime.utcnow()}},
        )

        sendMail(email, newToken, "New Verification Link Generated")

        return jsonify({"msg": "New Verification Link Sent", "success": True}), 200


userModel = User()
