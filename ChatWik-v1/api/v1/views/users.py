#!/usr/bin/python3
"""Handle API views for message.""" 
from api.v1.views import api_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from models import storage
from models.user import User


@api_views.route("/users", strict_slashes=False)
@swag_from("documentation/users/active_users.yml")
def all_users():
    """Retrieve all users."""
    users = storage.all(User).values()
    sorted_users = sorted(users, key=lambda user: user.is_active, reverse=True)
    user_list = [user.to_dict() for user in sorted_users]
    return jsonify(user_list)


@api_views.route("/users/<string:user_id>", strict_slashes=False)
@swag_from("documentation/users/all_users.yml")
def user(user_id):
    """Retrieve only active users."""
    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())
