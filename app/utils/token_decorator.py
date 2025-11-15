from flask import request, jsonify
from functools import wraps
from app.utils.jwt import decode_jwt_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        err_response = jsonify({
            "success": False,
            "message": "Unauthorized user"
        })
        token = request.cookies.get("token")
        if not token:
            return err_response, 400
        
        user_id = decode_jwt_token(token)
        if not user_id:
            return err_response, 400

        return f(user_id, *args, **kwargs)
    return decorated