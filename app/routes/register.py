from flask import Blueprint, jsonify, request, make_response
from app.extensions import db, bcrypt
from app.models.user import User
from app.utils.response import error_response
from sqlalchemy import Select
from app.utils.jwt import create_jwt_token

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=['POST'])
def register():
    try:
        body = request.get_json()
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        email = body.get("email")
        password = body.get("password")
        
        if not email or not first_name or not password:
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 404
            
        stmt = Select(User).where(User.email == email)
        is_exist = db.session.execute(stmt).scalar_one_or_none()
        
        if is_exist:
            return jsonify({
                "success": False,
                "message": "Email is already register, Please login to continue"
            }), 409
            
        hashed_pass = bcrypt.generate_password_hash(password, 10)
        
        new_user = User(
            firstname=first_name,
            lastname=last_name,
            email=email,
            password=hashed_pass
        )        
        db.session.add(new_user)
        db.session.commit()
        
        token = create_jwt_token(new_user.id)
        response = make_response(jsonify({
            "success": True,
            "message": "Account created successfully",
            "id": new_user.id,
            "first_name": new_user.firstname,
            "last_name": new_user.lastname,
            "email": new_user.email
        }))
        response.status_code = 201
        response.set_cookie("token", token, max_age=7*24*60*60, httponly=True, secure=True, path="/", samesite="None")
        
        return response
        
    except Exception as e:
        db.session.rollback()
        return error_response(e)