#!/usr/bin/python3
"""Models user login route."""
from api.v1.views import app_views
from flask import Blueprint, request, jsonify, render_template, session
from flasgger.utils import swag_from
from flask_jwt_extended import create_access_token
from models.user import User
from models import storage
from redis import Redis
from secrets import randbelow
import sib_api_v3_sdk
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from os import getenv


#------------------------LoginRoute---------------------------------#
@app_views.route("/auth/login", methods=["POST"])
@swag_from("documentation/auth/login.yml", methods=["POST"])
def login():
    """Defines the login routes of user."""
    data = request.get_json()

    if not data:
        return jsonify({"status": "Bad Request",
                        "message": "Empty request body"}), 400

    required_field = ["email", "password"]
    for field in required_field:
        if not data.get(field):
            return jsonify({"status": "Bad Request",
                            "message": f"{field} field require"}), 400

    email = data.get("email")
    password = data.get("password")

    sess = storage.get_session()

    user = sess.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        
        # Update user status to active once log in
        user.is_active = True
        storage.save()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            ),
            200
        )

    # Return for invalid credentials
    return jsonify({"status": "Unauthorized Access",
                    "message": "Invalide email or password"}), 401


# ---------------------SentTokenRoute----------------------------------#

r = Redis(host="localhost", port=6379, db=0)  # Connect to redis database


@app_views.route("/auth/send-token", methods=["POST"])
@swag_from("documentation/auth/send_token.yml", methods=["POST"])
def send_token():
    """Handle user registration."""
    data = request.get_json()

    # Check for empty request body
    if not data:
        error = {"status": "Bad Request",
                 "message": "Request body is empty"}
        return jsonify(error), 400

    # Check for required field
    required_field = ["name", "email"]
    for field in required_field:
        if not data.get(field):
            error = {"status": "Bad Request",
                     "message": f"{field} field require"}
            return jsonify(error), 400

    name = data.get("name")
    email = data.get("email")

    token = generate_token()

    # Sent token to recipient
    recipient = {"name": name, "email": email}
    response = send_token(token, "api/v1/views/email_content.html", **recipient)
    if response:
        return (
            jsonify(
                {
                    "status": "Success",
                    "token": token,
                    "message": "Confirmation code sent to email",
                }
            ),
            200,
        )
    return jsonify({"status": "Internal Error",
                    "message": "Token delivery failed"}), 500


#---------------------------RegisterRoute-----------------------------#

@app_views.route("/auth/register", methods=["POST"])
@swag_from("documentation/auth/register.yml", methods=["POST"])
def register():
    """Complete user registration."""
    data = request.get_json()

    # Check for empty request body
    if not data:
        error = {"status": "Bad Request", "message": "Request body is empty"}
        return jsonify(error), 400

    # Check for password
    required_field = ["name", "email", "password", "token"]
    for field in required_field:
        if not data.get(field):
            error = {"status": "Bad Request",
                     "message": f"{field} field required"}
            return jsonify(error), 400

    # Check if token is valid
    token = data.get("token")
    retrieved_token = r.get(token)
    if not retrieved_token:
        error = {"status": "Validation Error",
                 "message": "Invalid or expired token"}
        return jsonify(error), 422

    # Create an instance of User class
    attribute = {
        "name": data.get("name"),
        "username": data.get("username"),
        "email": data.get("email"),
        "password": data.get("password"),
    }
    user = User(**attribute)
    try:
        if retrieved_token:
            user.hash_password()
            storage.new(user)
            storage.save()

            # Delete token after confirmation
            r.delete(token)

            return (
                jsonify(
                    {
                        "status": "Success",
                        "message": "Registration successfully",
                        "data": {
                            "id": user.id,
                            "first_name": user.name,
                            "last_name": user.name,
                            "email": user.email,
                            "password": user.password,
                            "username": user.username
                        },
                    }
                ),
                201,
            )
    except IntegrityError:
        session = storage.get_session()
        error = {"status": "User already exists",
                 "message": "Email is already registered"}
        session.rollback()
        return jsonify(error), 409
    finally:
        storage.close()


#-----------------------FunctionDefinition--------------------------#

def generate_token():
    """Create a 6-digit token on every call."""
    token = str(randbelow(900000) + 100000)
    expiring_time = timedelta(minutes=15)

    # Save token to redis db and delete when expiring time ellapsed
    # The key of this token is the token itself
    r.setex(token, expiring_time, "valid")
    return token


def send_token(token, email_file, **recipient):
    """Send token to email.

    Args:
        token (string): The 6-digit email confirmation token.
        email_file (string): Path to email template file.
        kwargs (dict): Key-value pairs of recipient info.
    """
    config = sib_api_v3_sdk.Configuration()
    config.api_key["api-key"] = getenv("MAIL_API_KEY")

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(config)
    )

    sender = {"name": "Wikkisoft Company", "email": "wisdomokposin@gmail.com"}
    email_subject = "[AGS] Complete your registration"
    recipient = [recipient]

    recipient_name = recipient[0]["name"]
    email_content = read_email(email_file, token, recipient_name)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=recipient, sender=sender, subject=email_subject,
        html_content=email_content
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except Exception:
        return False


def read_email(file_path, token, name):
    """Read email from file and substitue placeholder."""
    with open(file_path, "r") as file:
        content = file.read()
    content = content.replace("{{ name }}", name).replace("{{ token }}", token)
    return content
