from flask import jsonify

def error_response(e):
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "error": str(e)
    }), 500