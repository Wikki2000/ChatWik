#!/usr/bin/python3
""" Create Flask Application. """
from api.v1.config import Config
from flask import Flask, jsonify
from flasgger import Swagger
from os import getenv
from api.v1.views import app_views
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask_wtf.csrf import generate_csrf

# Setting up Flask Application.
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(app_views)

# Initialization of Fask Application.
JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
Swagger(app)


@app.route('/get-csrf-token', methods=['GET'])
def get_csrf_token():
    return jsonify({"csrf_token": generate_csrf()})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error in the application scope."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
