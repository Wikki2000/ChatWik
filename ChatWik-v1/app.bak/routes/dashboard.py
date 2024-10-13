#!/usr/bin/python3
""" Model for handling views for user dashboard. """
from app.routes import app_views
from flask import render_template, request
from flask_jwt_extended import jwt_required
import requests
from uuid import uuid4


@app_views.route("/dashboard", strict_slashes=False)
@jwt_required()
def dash_board():
    """Handle view for dash board."""
    return render_template("dashboard.html")
