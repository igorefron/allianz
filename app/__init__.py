from flask import Flask
from .routes import bp as routes_bp

#import secrets

def create_app():
    app = Flask(__name__)

    # Register the routes blueprint
    app.register_blueprint(routes_bp)

    return app
