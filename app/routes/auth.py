#!/usr/bin/python3
"""Handle Views of Authentication."""
from flask import render_template, session
from app.routes import app_views


AUTH_TEMPLATES_DIRECTORY = "/auth"


@app_views.route("/account/login")
def login():
    """Render template to login user."""
    return render_template(f"{AUTH_TEMPLATES_DIRECTORY}/login.html")


@app_views.route("/account/register")
def register():
    """Render template for user registration."""
    return render_template(f"{AUTH_TEMPLATES_DIRECTORY}/registration.html")

@app_views.route("/account/verify")
def verify():
    """Render template for email verification."""
    print(session.get("reg_data").get("email"))
    email = session.get("reg_data", {}).get("email")
    return render_template(
        f"{AUTH_TEMPLATES_DIRECTORY}/verify_email.html", email=email
    )
