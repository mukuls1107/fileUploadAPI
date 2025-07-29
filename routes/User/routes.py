from flask import Blueprint, jsonify, request, session
import bcrypt, jwt, os
from datetime import datetime, timedelta
from functools import wraps

# from models import userModel
from .models import userModel

userRoutes = Blueprint("users", __name__)


def token_required(token):
    # if 'token' in 
    pass

@userRoutes.route("/public", methods=["GET"])
def public():
    return "JWT Verified! Hello User"


@userRoutes.route("/signup", methods=["POST"])
def registerUser():
    data = request.get_json()
    
    if not data["email"] or not data["password"] or not data["userType"]:
        return jsonify({"success": False, "msg": "Incomplete details"}), 400

    if userModel.checkUserPresent(data["email"]):
        return jsonify({"msg": "User is already Present", "success": False}), 400

    dbResponse = userModel.createUser(
        email=data["email"], password=data["password"], userType=data["userType"]
    )
    # print(data)

    return dbResponse


@userRoutes.route("/verify/<token>", methods=["GET"])
def verifyUserEmail(token):
    print(token)
    result = userModel.verifyEmail(token)
    return result
    # return "Verification Route hit"


@userRoutes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data["email"] or not data["password"]:
        return (
            jsonify({"success": False, "msg": "missing email or password"}),
            400,
        )

    email = data["email"].lower().strip()
    password = data["password"]

    if userModel.checkUserPresent(email):
        userData = userModel.getUserInfo(email)

        checkPassword = bcrypt.checkpw(password.encode(), userData["passwordHash"])

        if checkPassword:
            if userData["isVerified"]:
                askedData = {
                    "id": str(userData["_id"]),
                    "email": userData["email"],
                    "userType": userData["userType"],
                    "isVerified": userData["isVerified"],
                }

                jwtToken = jwt.encode(
                                    {
                                        "user": askedData["email"],
                                        "expiration": str(datetime.utcnow() + timedelta(hours=24)), # <--- CHANGED
                                    },
                                    os.getenv("JWT_KEY"),
                                )

                session["access_token"] = jwtToken
                userModel.addTokeninUser(askedData["email"], jwtToken)
                
                
                return (
                    jsonify(
                        {
                            "msg": "logged in successfully",
                            "success": True,
                            "user": askedData,
                            "token": jwtToken,
                        }
                    ),
                    200,
                )
            else:
                userModel.resendVerification(email)
                return (
                    jsonify(
                        {
                            "msg": "user is not verified, verification link sent again!",
                            "success": False,
                        }
                    ),
                    403,
                )
        else:
            return (
                jsonify(
                    {
                        "msg": "Invalid email or password",
                        "success": False,
                    }
                ),
                401,
            )
    else:
        return (
            jsonify(
                {
                    "msg": "User not found",
                    "success": False,
                }
            ),
            404,
        )
