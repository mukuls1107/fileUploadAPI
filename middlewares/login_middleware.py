import functools
from flask import session, jsonify, request
from routes.User.models import userModel


def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if "access_token" not in session:
            return (
                jsonify(
                    {
                        "msg": "Access token not found",
                        "success": False,
                    }
                ),
                404,
            )

        else:
            token = session.get("access_token")
            if userModel.getUserAccessToken(token=token):
                # pass
                request.user = token
                return view_func(*args, **kwargs)
                # return jsonify({"msg": "User found", "success": True}), 200
            else:
                return (
                    jsonify(
                        {
                            "msg": "User is not logged in or the access token is incorrect",
                            "success": False,
                        }
                    ),
                    400,
                )

    return decorated

def authForAdmin(role):
    def decorator(view_func):
        @functools.wraps(view_func)
        def decorated(*args, **kwargs):
            if "access_token" not in session:
                return jsonify({"msg": "Access token not found", "success": False}), 404

            token = session.get("access_token")
            user = userModel.getUserAccessToken(token=token)

            if not user:
                return jsonify({"msg": "Access Denied", "success": False}), 401
                # return jsonify({"msg": "User found", "success": True}), 200

            userRole = userModel.getUserRoleFromToken(token)

            if userRole.lower() != "ops":
                return jsonify({"msg": "Access restricted to " + userRole, "success": False}), 403

            request.user = user
            return view_func(*args, **kwargs)

        return decorated  
    return decorator