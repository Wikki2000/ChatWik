#!/usr/bin/python3
""" Model for handling views for user dashboard. """
from app.routes import app_views
from app.routes.utils import safe_api_request, get_auth_headers
from flask import render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from uuid import uuid4

API_BASE_URL = 'http://127.0.0.1:5002/api/v1'


@app_views.route(f"/dashboard")
@jwt_required()
def dashboard():
    """Handle views for user dashboard."""
    headers = get_auth_headers()
    if not headers:
        return jsonify({"error": "Missing or Invalid Access Token"}), 401
    user_id = get_jwt_identity()
    url  = API_BASE_URL + f"/users/{user_id}"
    json_response, status_code = safe_api_request(url, "GET", headers=headers)
    email = json_response.get("email")
    first_name = json_response.get("first_name")
    last_name = json_response.get("last_name")
    state = json_response.get("state")
    data = {"email": email, "first_name": first_name, "state": state,
            "last_name": last_name, "cache_id": uuid4()}
    return render_template("user_dashboard.html", **data)


@app_views.route(f"/friends/<string:friend_id>/chat")
@jwt_required()
def chat(friend_id):
    """Render pages for chatting and pass friend ID to chat page

    :friend_id: The friend ID to be pass to next chat  page/
    """
    data = {"cache_id": uuid4(), "friend_id": friend_id}
    return render_template("chat.html", **data)



@app_views.route(f"/friends/<string:friend_id>/profile")
@jwt_required()
def friend_profile(friend_id):
    return render_template("friend_profile.html", friend_id=friend_id)
