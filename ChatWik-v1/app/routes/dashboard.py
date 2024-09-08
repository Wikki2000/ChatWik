#!/usr/bin/python3
""" Model for handling views for user dashboard. """
from app.routes import app
from flask import render_template, request
from flask_jwt_extended import jwt_required
import requests
from uuid import uuid4

URL_PREFIX="/chatwik"

@app.route(f"{URL_PREFIX}/dashboard", strict_slashes=False)
@jwt_required()
def dash_board():
    """Handle view for dash board."""
    if request.method == "GET":
        display_name = request.args.get("display_name")
        return render_template("dash_board.html", display_name=display_name)
