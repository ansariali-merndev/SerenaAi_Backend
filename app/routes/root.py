from flask import Blueprint, jsonify
from app.utils.response import error_response

root_bp = Blueprint("root", __name__)

@root_bp.route("/", methods=['GET', 'POST', 'PUT', 'PATCH'])
def root():
    try:
        return jsonify({
            "success": True,
            "message": "Welcome to the flask application"
        }), 200
    except Exception as e:
        return error_response(e)