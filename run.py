from app import create_app
from app.extensions import db

server = create_app()

with server.app_context():
    db.create_all()

if __name__ == "__main__":
    server.run(debug=True)