#!/usr/bin/python3
"""Handle Views of Authentication."""
from flask import render_template, url_for, redirect
from app.routes import app_views
from app.routes import web_static


AUTH_TEMPLATES_DIRECTORY = ""


@web_static.route("/web_static/<string:page>")
def static(page):
    """Render template to login user."""
    return render_template(f"{AUTH_TEMPLATES_DIRECTORY}{page}.html")
