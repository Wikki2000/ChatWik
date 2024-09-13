#!/usr/bin/python3
"""Handle API views for message.""" 
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from models import storage
from models.user import User


@app_views.route("/all-users", strict_slashes=False)
@swag_from("documentation/users/active_users.yml")
def all_users():
    """Retrieve all users."""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route("/active-users", strict_slashes=False)
@swag_from("documentation/users/all_users.yml")
def active_users():
    """Retrieve only active users."""
    users = storage.all(User).values()

    # Use list comprehension to filter active user
    active_users = [user for user in users if user.is_active]
    user_list = [user.to_dict() for user in active_users]
    return jsonify(user_list)
