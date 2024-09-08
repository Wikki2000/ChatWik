#!/usr/bin/python3
"""Start a Flask Web Application."""
from app.routes import app
from flask import Flask, render_template, session, request, jsonify, abort
from flask_jwt_extended import set_access_cookies
from uuid import uuid4
import requests
from requests.exceptions import ConnectionError, Timeout
from redis import Redis
from datetime import timedelta
from os import getenv


URL_PREFIX = "/chatwik"
@app.route(f"{URL_PREFIX}", strict_slashes=False)
def home():
    """Redirect user to login route."""
    return redirect(url_for("login"))


@app.route(
        f"{URL_PREFIX}/account/signin",
        methods=["GET", "POST"],
        strict_slashes=False
)
def login():
    """Handle view for login."""
    if request.method == "GET":
        return render_template("login.html", cache_id=uuid4())

    # Sent request to login API to validate user credentials.
    form_data = request.get_json()
    request_body = {"email": form_data.get("email"),
                    "password": form_data.get("password")}
    url = "http://127.0.0.1:5001/api/v1/auth/login"
    response = requests.post(url, json=request_body)
    data = response.json()

    # Important user data needed throughout the application.
    access_token = data.get("access_token")
    name = data.get("user", {}).get("name")
    user_name = data.get("user", {}).get("user_name")
    if response.status_code == 200:
        json_res = jsonify(data)
        set_access_cookies(json_res, access_token)
        session.clear()
        return json_res, 200
    elif response.status_code == 401:
        return jsonify({"error": "Invalid Password or Email"}), 401


@app.route(
    f"{URL_PREFIX}/account/verify",
    methods=["POST"],
    strict_slashes=False
)
def verify():
    """Handle view for email verification and,
    send request to API to permanently store user data.
    """
    # Add token to temporarily stored user data in session
    token_dict = request.get_json()
    data = session.get("registration_data")

    if not data:
        abort(400, "session data not set")

    data["token"] = token_dict.get("token")

    # Sent the data to register api to be stored permannently.
    url = "http://127.0.0.1:5001/api/v1/auth/register"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    return jsonify({"error": "Something Went Wrong"}), 500


@app.route(f"{URL_PREFIX}/account/verify-success", strict_slashes=False)
def verify_success():
    """Handle view for email verification success."""
    return render_template("verify-success.html", cache_id=uuid4())


@app.route(
    f"{URL_PREFIX}/account/signup",
    methods=["GET", "POST"],
    strict_slashes=False
)
def register():
    """Handle Registration View of Application."""
    if request.method == "GET":
        return render_template("registration.html", cache_id=uuid4())

    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    data = {
        "first_name": first_name,
        "username": username,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    full_name = first_name + " " + last_name
    # Temporarily store form data in redis and redirect.
    # To verify email before saving permanently in database.
    session["registration_data"] = data
    url = "http://127.0.0.1:5001/api/v1/auth/send-token"
    request_body = {"name": full_name, "email": email}
    response = requests.post(url, json=request_body)
    if response.status_code == 422:
        return jsonify({"error": "User Exists Already"}), 422
    elif response.status_code == 200:
        return jsonify(
                {
                    "status": "Success",
                    "msg": "Registration Successful"
                }
        ), 200
    else:
        return jsonify({"error": "Something Went Wrong"}), 500


#------------------------------FunctionsDefinition--------------------------#

def get_request(url):
    """
    Handle get request of given url.
    Return (JSON): The JSON data from request.
    """
    try:
        response = requests.get(url, timeout=15) # Set timeout to 15 secs
        return response.json()
    except ConnectionError:
        return jsonify({"status": "Request Timeout",
                        "message": "API Connection Failed"})
    except Timeout:
        return jsonify({"status": "Request Timeout",
                        "msg": "Request Timeout. Try Again Later"})

        
if __name__ == "__main__":
    app.run(debug=True, port=5000)
