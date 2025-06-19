from flask import Blueprint, jsonify, request

# from models import userModel
from .models import userModel

userRoutes = Blueprint("users", __name__)


@userRoutes.route("/signup", methods=["POST"])
def registerUser():
    data = request.get_json()

    if not data["email"] or not data["password"] or not data["userType"]:
        return jsonify({"success": False, "msg": "Incomplete details"}), 400

    
    dbResponse = userModel.createUser(
        email=data["email"], 
        password=data["password"],
        user_type=data["userType"]
    )
    # print(data)
    return dbResponse
