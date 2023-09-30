from flask import Flask
from .routes import bp as routes_bp

#import secrets

def create_app():
    app = Flask(__name__)

    app.secret_key = 'UnQ0NqRUwhuBtCLDCbA6Lo1NtA'  # Replace with your actual secret key

    # Register the routes blueprint
    app.register_blueprint(routes_bp)

    return app
