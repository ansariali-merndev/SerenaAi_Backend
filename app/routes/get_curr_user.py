from flask import Blueprint, request, jsonify
from app.utils.response import error_response
from app.utils.jwt import decode_jwt_token
from sqlalchemy import Select
from app.models.user import User
from app.extensions import db

get_curr_user_bp = Blueprint("get_curr_user", __name__)

@get_curr_user_bp.route("/get_curr_user")
def get_curr_user():
    try:
        token = request.cookies.get("token")
        
        if not token:
            return jsonify({
                "success": False,
                "message": "Token not found"
            }), 404
        
        user_id = decode_jwt_token(token)
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 404
        stmt = Select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid Token"
            }), 400
            
        return jsonify({
            "success": True,
            "id": user.id,
            "first_name": user.firstname,
            "last_name": user.lastname,
            "email": user.email
        })
    except Exception as e:
        return error_response(e)