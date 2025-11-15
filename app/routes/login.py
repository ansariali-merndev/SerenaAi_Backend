from flask import Blueprint, request, jsonify, make_response
from app.utils.response import error_response
from app.models.user import User
from sqlalchemy import Select
from app.extensions import db, bcrypt
from app.utils.jwt import create_jwt_token

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=['POST'])
def login():
    login_err = jsonify({
        "success": False,
        "message": "Invalid credential"
    })
    try:
        body = request.get_json()
        email = body.get("email")
        password = body.get("password")
        
        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Please fill the all required fields"
            }), 404
            
        stmt = Select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar_one_or_none()
        
        if not user:
            return login_err, 404
        
        is_pass_match = bcrypt.check_password_hash(user.password, password)
        if not is_pass_match:
            return login_err, 404
        
        token = create_jwt_token(user.id)
        response = make_response(jsonify({
            "success": True,
            "message": "Login successfully",
            "id": user.id,
            "first_name": user.firstname,
            "last_name": user.lastname,
            "email": user.email
        }))
        
        response.status_code = 200
        response.set_cookie("token", token, max_age=7*24*60*60, httponly=True, secure=True, path="/", samesite="None")
        
        return response
        
    except Exception as e:
        return error_response(e)