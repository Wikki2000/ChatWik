#!/usr/bin/python3
"""
Defines configuration settings for the Flask application.

The `Config` class serves as the base configuration, providing default settings
that can be inherited and overridden by environment-specific configurations.

Key configurations include:

- SECRET_KEY: Use for session management and other security-related features.
- SWAGGER: Use for Swagger UI, including the title and UI version.
"""
from os import getenv


class Config:
    """Base configuration."""
    SECRET_KEY = getenv("FLASK_SECRET_KEY")
    SWAGGER = {"title": "ChatWik RESTful API", "uiversion": 3}
    WTF_CSRF_ENABLED = False
