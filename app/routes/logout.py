from flask import Blueprint, jsonify, make_response
from app.utils.response import error_response

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout")
def logout():
    try:
        response = make_response(jsonify({
            "success": True,
            "message": "logout successfully"
        }))
        response.status_code = 200
        response.delete_cookie("token")
        
        return response
    except Exception as e:
        return error_response(e)