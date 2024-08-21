#!/usr/bin/python3
"""Handle index view of API."""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Check status of API."""
    return jsonify({"status": "OK"}), 200
