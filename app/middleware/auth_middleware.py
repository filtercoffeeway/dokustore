from functools import wraps
from flask import request, current_app
import jwt
from app.daos.user import UserDAO

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-auth-token" in request.headers:
            token = request.headers["x-auth-token"]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=UserDAO.get_user_by_auth_token(data['auth_token'])
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            if not current_user.status == 'active':
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 403
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated