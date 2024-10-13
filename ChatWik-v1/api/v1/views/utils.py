#!/usr/bin/python3
"""This modules defines helper function for API"""
from api.v1.views import api_views
from flask import request, jsonify
from datetime import timedelta
from os import getenv
import sib_api_v3_sdk
from redis import Redis
from random import randint
from dotenv import load_dotenv

load_dotenv()
r = Redis(host="localhost", port=6379, db=0)


def send_token(name, email):
    """Handle view for sending of token."""

    # Genrate token and store in redis db temporarily
    token = generate_token()
    mins = 60
    expiring_time = timedelta(minutes=mins)
    r.setex(token, expiring_time, "valid")

    # Send token to user for email verification
    recipient = {"name": name, "email": email}
    file_path = "api/v1/views/auth/email_content.html"
    email_content = read_html_file(file_path, recipient["name"], token)
    response = fwd_token(token, email_content, recipient)
    if response:
        return {
            "status": "Success",
            "token": token,
            "expiring_time": f"{mins} minute"
        }
    return {"error": "Token Delivery Failed"}


def generate_token():
    """Return a 6 digit random numbers."""
    return str(randint(100000, 999999))


def fwd_token(token, mail, kwargs):
    """Send token to email.

    Args:
        token (string): The 6-digit email confirmation token.
        mail (string): The mail to be sent.
        kwargs (dict): Key-value pairs of recipient info.
    """
    config = sib_api_v3_sdk.Configuration()
    config.api_key["api-key"] = getenv("MAIL_API_KEY")
    SENDER_MAIL = getenv("SENDER_MAIL")
    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(config)
    )

    sender = {"name": "WIS_Grader", "email": getenv("SENDER_EMAIL")}
    email_subject = "[Wis_Grader] Complete your registration"
    recipient = [kwargs]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=recipient, sender=sender, subject=email_subject,
        html_content=mail
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    except Exception:
        return False


def read_html_file(file_path, name, token):
    """Read email from file and substitue placeholder."""
    with open(file_path, "r") as f:
        content = f.read()

    # Replace content with placeholder
    content = content.replace("{{ name }}", name).replace("{{ token }}", token)
    return content
