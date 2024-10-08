#!/usr/bin/python3
""" Create Flask Application. """
from app.config import Config
from app.routes import app as bp
from flask import Flask, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager
import os

# Setting up Flask Application.
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the JWT Manager
jwt = JWTManager(app)

# Register blueprint
app.register_blueprint(bp)


# Handle expired tokens
"""
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # Redirect to login page on token expiry
    return redirect(url_for('app.login'))
"""

@app.errorhandler(404)
def not_found(error):
    """Handle 404 error in the application scope."""
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
