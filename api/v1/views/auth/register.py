#!/usr/bin/python3
"""This API Handles Registration of User."""
from api.v1.views import api_views, utils
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import request, jsonify, session
from flasgger.utils import swag_from
from redis import Redis
from models.user import User
from models import storage
from sqlalchemy.exc import IntegrityError

r = Redis(host="localhost", port=6379, db=0)


@api_views.route("/account/register", methods=["POST"])
@swag_from("../documentation/auth/register.yml")
def register():
    """Handle view for registration of user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad Request"}), 400

    required_fields = [
        "first_name", "last_name", "email", 
        "password", "country", "state"
    ]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} Field Missing"}), 400

    if storage.get_by_field(User, "email", data["email"]):
        return jsonify({"error": "Email Exists Already"}), 409

    session["reg_data"] = data

    first_name = data["first_name"] + " " + data["last_name"]

    # Return response in json of the dict returns of the function
    response = utils.send_token(first_name, data["email"])
    print(response)
    return jsonify(response)
    

@api_views.route("/account/verify", methods=["POST"])
@swag_from("../documentation/auth/register.yml")
def verify():
    """Verify if email is valid."""

    # Check if "token" in request body
    token = request.get_json().get("token")
    if not token:
        return jsonify({"error": "Missing token Field"}), 400

    # Validate token by checking if still in redis database
    if not r.get(token):
        return jsonify({"error": "Invalid or Expired Token"}), 422

    try:
        print(session["reg_data"])
        if "reg_data" not in session:
            return jsonify({"error": "Session Data not Set"}), 400
        user = User(**session["reg_data"])
        user.hash_password()
        storage.new(user)
        storage.save()
        r.delete(token)
        response = jsonify({
            "status": "Success",
            "msg": "Registration Successful"
        })
        access_token = create_access_token(identity=user.id)
        set_access_cookies(response, access_token)
        return response
    except IntegrityError:
        storage.rollback()
        return jsonify({"error": "User Exists Already"}), 409
    finally:
        storage.close()
