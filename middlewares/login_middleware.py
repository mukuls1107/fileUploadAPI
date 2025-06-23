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