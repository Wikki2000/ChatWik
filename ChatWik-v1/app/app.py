#!/usr/bin/python3
"""Start a Flask Web Application."""
from flask import Flask, render_template, redirect, url_for, session, request, jsonify, abort, flash, make_response
from flask_jwt_extended import jwt_required, JWTManager
from uuid import uuid4
import requests
from redis import Redis
from datetime import timedelta
from os import getenv

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("FLASK_SECRET_KEY")
jwt = JWTManager(app)

URL_PREFIX = "/ChatWik/v1"
@app.route(f"{URL_PREFIX}", strict_slashes=False)
def home():
    """Redirect home to login page."""
    return redirect(url_for("login"))


@app.route(
        f"{URL_PREFIX}/auth/login",
        methods=["GET", "POST"],
        strict_slashes=False
)
def login():
    """Handle view for login."""
    if request.method == "GET":
        return render_template("login.html", cache_id=uuid4())

    # Sent request to login API to validate user credentials.
    form_data = request.form
    request_body = {"email": form_data.get("email"),
                    "password": form_data.get("password")}
    url = "http://127.0.0.1:5001/api/v1/auth/login"
    response = requests.post(url, json=request_body)
    response_data = response.json()
    if response.status_code != 200:
        error_message = response_data.get("message")
        flash(error_message)
        return render_template("login.html")

    # Important user needed throughout the application.
    access_token = response_data.get("access_token")
    user_id = response_data.get("user", {}).get("id")
    name = response_data.get("user", {}).get("name")
    user_name = response_data.get("user", {}).get("user_name")


    display_name = user_name if user_name else name

    # Create response object and use it to set authorisation header in cookie.
    # Without using max_age or expires, the cookie elapse once the browser is close.
    response = make_response(redirect(url_for('dash_board', display_name=display_name)))
    response.set_cookie("access_token_cookie", access_token, httponly=True, secure=True)

    session["user_id"] = user_id

    # Delete the temporary store user data from session.
    # After successful email verication and login in.
    session.pop("registration_data", None)
    return response


@app.route(
    f"{URL_PREFIX}/dash-board",
    methods=["GET", "POST"],
    strict_slashes=False
)
@jwt_required(locations=['cookies'])
def dash_board():
    """Handle view for dash board."""
    if request.method == "GET":
        display_name = request.args.get("display_name")
        return render_template("dash_board.html", display_name=display_name)


@app.route(
    f"{URL_PREFIX}/auth/verify-email",
    methods=["GET", "POST"],
    strict_slashes=False
)
def verify_email():
    """Handle view for email verification and,
    send request to API to permanently store user data.
    """
    if request.method == "GET":
        email = request.args.get("email")
        data = {"cache_id": uuid4(), "email": email}
        return render_template("verify-email.html", data=data)

    # Add token to temporarily stored user data in session
    token_dict = request.get_json()
    data = session.get("registration_data")

    if not data:
        abort(400, "session data not set")

    data["token"] = token_dict.get("token")

    # Sent the data to register api to be stored permannently.
    url = "http://127.0.0.1:5001/api/v1/auth/register"
    response = requests.post(url, json=data)
    return response.json()


@app.route(f"{URL_PREFIX}/auth/verify-success", strict_slashes=False)
def verify_success():
    """Handle view for email verification success."""
    return render_template("verify-success.html", cache_id=uuid4())


@app.route(
        f"{URL_PREFIX}/auth/register",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def register():
    """Handle Registration View of Application."""
    if request.method == "GET":
        return render_template("registration.html", cache_id=uuid4())

    data = request.form
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    data = {"name": name, "username": username,
            "email": email, "password": password}
    # Temporarily store form data in redis and redirect.
    # To verify email before saving permanently in database.
    session["registration_data"] = data
    url = "http://127.0.0.1:5001/api/v1/auth/send-token"
    request_body = {"name": data.get("name"), "email": data.get("email")}
    response = requests.post(url, json=request_body)
    if response.status_code != 200:
        abort(500, "Failed to conect to API")

    return redirect(url_for('verify_email', email=email))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
