#!/usr/bin/python3
"""Sign in user with valid credentials."""
from flask import request, jsonify
from models.user import User
from flask_jwt_extended import create_access_token, set_access_cookies
import datetime
from api.v1.views import api_views
from models.storage import Storage
from models import storage
from flasgger.utils import swag_from


@api_views.route('/account/login', methods=['POST'])
@swag_from('../documentation/auth/login.yml')
def login():
    """Route for user login with JSON data."""

    # Parse JSON data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Ensure all required fields are in the JSON data
    required_fields = ['email_or_username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            "error": f"{''.join(missing_fields)} Field Missing"
        }), 400

    email_or_username = data['email_or_username']
    password = data['password']

    storage = Storage()
    session = storage.get_session()

    # Check if the user signs in by email or username
    users = storage.get_by_field(User, "email", email_or_username) \
            if "@" in email_or_username \
            else storage.get_by_field(User, "username", email_or_username)

    for user in users:
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
    user.is_active = True
    storage.save()

    # Create JWT token
    access_token = create_access_token(identity=user.id)

    # Return response with aceess token
    response =  jsonify(
        {
            "message": "Login successful",
            "status": "Success",
            "access_token": access_token,
            "user":
                {
                    "email": user.email,
                    "id": user.id,
                    "username": user.username,
                    "name": user.first_name + " " + user.last_name,
                    "profile_photo": user.profile_photo
                }
        }
    )
    set_access_cookies(response, access_token)  # Set JWT in cookie
    return response
