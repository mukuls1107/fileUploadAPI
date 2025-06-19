from flask import Blueprint, jsonify, request

# from models import userModel
from .models import userModel

userRoutes = Blueprint("users", __name__)


@userRoutes.route("/signup", methods=["POST"])
def registerUser():
    data = request.get_json()

    
    if not data["email"] or not data["password"] or not data["userType"]:
        return jsonify({"success": False, "msg": "Incomplete details"}), 400

    if userModel.checkUserPresent(data["email"]):
            return jsonify({"msg": "User is already Present", "success": False}), 400

    
    dbResponse = userModel.createUser(
        email=data["email"], 
        password=data["password"],
        userType=data["userType"]
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
def login(self):
    return
    
     