import functools
from flask import session, jsonify, request
from routes.User.models import userModel
import jwt # Import jwt library
import os
from datetime import datetime

def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        token = None
        # 1. Try to get token from session (for browser-based users)
        if "access_token" in session:
            token = session.get("access_token")
        # 2. If not in session, try to get token from Authorization header (for API clients like iOS Shortcut)
        elif "Authorization" in request.headers:
            try:
                auth_header = request.headers["Authorization"]
                # Expected format: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"msg": "Authorization header format invalid", "success": False}), 400

        if not token:
            return jsonify({"msg": "Access token not found", "success": False}), 401 # Use 401 for missing token

        try:
            # Decode and verify the JWT token
            # Ensure you use the correct algorithm (HS256 is common for Flask-JWT)
            decoded_token = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])

            # Check the custom 'expiration' field you embedded in the JWT
            # Note: datetime.strptime requires the exact format string from where you created it
            expiration_time = datetime.strptime(decoded_token["expiration"], "%Y-%m-%d %H:%M:%S.%f")
            if datetime.utcnow() >= expiration_time:
                 return jsonify({"msg": "Token has expired", "success": False}), 401

            # Optionally, you can also check if the token is still active in your DB (as you currently do)
            # This adds an extra layer of security, allowing you to revoke tokens server-side.
            user_token_data = userModel.getUserAccessToken(token=token)

            if user_token_data:
                # If authentication is successful, set request.user to the email from the token
                request.user = decoded_token["user"]
                return view_func(*args, **kwargs)
            else:
                # If the token is valid but not found/active in DB (e.g., revoked, or DB check failed)
                return jsonify({"msg": "Invalid or inactive access token", "success": False}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token has expired", "success": False}), 401
        except jwt.InvalidTokenError:
            # This handles various JWT errors (e.g., malformed token, incorrect signature)
            return jsonify({"msg": "Invalid token", "success": False}), 401
        except Exception as e:
            # Catch any other unexpected errors during token processing
            print(f"Authentication error: {e}") # Good for debugging
            return jsonify({"msg": "Authentication failed due to server error", "success": False}), 500

    return decorated


def authForAdmin(role):
    def decorator(view_func):
        @functools.wraps(view_func)
        def decorated(*args, **kwargs):
            # The 'auth' middleware should have already validated the token
            # and set request.user to the user's email.
            # If auth fails, it will return a response before this decorator runs.

            user_email = request.user # Get user email from the request context

            if not user_email:
                # This case should ideally not happen if @auth ran successfully
                return jsonify({"msg": "Authentication context missing", "success": False}), 401

            # Retrieve the user's role from the database using their email
            # It's more reliable to get the current role from DB rather than from an potentially outdated token payload
            user_data = userModel.getUserInfo(user_email)

            if not user_data:
                return jsonify({"msg": "User not found for role check", "success": False}), 404

            userRole = user_data.get("userType") # Get the userType from the fetched user data

            if userRole and userRole.lower() == role.lower(): # Compare roles case-insensitively
                return view_func(*args, **kwargs)
            else:
                return jsonify({"msg": f"Access restricted to users with '{role}' role. Your role is '{userRole}'.", "success": False}), 403

        return decorated  
    return decorator