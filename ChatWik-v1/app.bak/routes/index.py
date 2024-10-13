#!/usr/bin/python3
"""Handle API views."""
from flask import jsonify, redirect, url_for
from app.routes import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"}), 200


@app_views.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 400

@app_views.app_errorhandler(401)
def unauthorize(error):
    return redirect(url_for('app_views.login'))
