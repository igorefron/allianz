from flask import Flask
from typing import Any
from .routes import bp as routes_bp
import os

def create_app() -> Flask:
    app = Flask(__name__)

    # Load secret key from environment variable
    app.secret_key = 'UnQ0NqRUwhuBtCLDCbA6Lo1NtA'

    # Register the routes blueprint
    app.register_blueprint(routes_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error: Any) -> Any:
        return "Resource not found", 404

    @app.errorhandler(500)
    def internal_error(error: Any) -> Any:
        return "Internal server error", 500

    return app
