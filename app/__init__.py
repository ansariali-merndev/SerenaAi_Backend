from flask import Flask
from flask_cors import CORS
from app.extensions import db, bcrypt
from app.env import DB_URI, FRONTEND_URI
from app.routes.root import root_bp
from app.routes.register import register_bp
from app.routes.login import login_bp
from app.routes.logout import logout_bp
from app.routes.talk import talk_bp
from app.routes.get_curr_user import get_curr_user_bp
from app.routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    CORS(app=app, origins=FRONTEND_URI, supports_credentials=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    list_bp = [root_bp, register_bp, logout_bp, login_bp, talk_bp, get_curr_user_bp, dashboard_bp]
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    for bp in list_bp:
        app.register_blueprint(bp)
    
    return app