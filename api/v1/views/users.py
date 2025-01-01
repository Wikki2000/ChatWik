#!/usr/bin/python3
"""Handle API views for message.""" 
from api.v1.views import api_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from models import storage
from models.user import User


@api_views.route("/users/<string:user_id>", strict_slashes=False)
@swag_from("documentation/users/all_users.yml")
def user(user_id):
    """Retrieve data of a User using his ID."""

    user = storage.get_by_id(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())
