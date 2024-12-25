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
from models import storage
from models.friend import Friend
from typing import Dict, Union, Optional
from models.private_message import PrivateMessage


load_dotenv()
r = Redis(host="localhost", port=6379, db=0)


# =================================================== #
#           Authentication Helper Function            #
# =================================================== #
def send_token(name: str, email: str) -> Dict[str, str]:
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


def generate_token() -> str:
    """Return a 6 digit random numbers."""
    return str(randint(100000, 999999))


def fwd_token(token: str, mail: str, kwargs: Dict[str, str]) -> bool:
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


def read_html_file(file_path: str, name: str, token: str) -> str:
    """Read email from file and substitue placeholder."""
    with open(file_path, "r") as f:
        content = f.read()

    # Replace content with placeholder
    content = content.replace("{{ name }}", name).replace("{{ token }}", token)
    return content


# ========================================================= #
#               Friends Module Helper Function              #
# ========================================================= #
def is_friend(user_id: str, friend_id: str) -> bool:
    """
    Check if there’s no friendship,
    i.e., is_friend is False or request doesn’t exist

    :user_id - The current user_id
    :friend_id - The friend ID to check friendship

    :rtype - True if friendship exists, else false.
    """
    friend_request = storage.get_by_double_field(
        Friend, ["sender_id", user_id], ["reciever_id", friend_id]
    )
    if not friend_request or any(
        req.is_friend is False for req in friend_request
    ):
        return False
    return True


def friendship(user_id: str, friend_id: str) -> Union[bool, Friend]:
    """
    Get friendship object b/w user and friend

    :user_id - The current user_id
    :friend_id - The friend ID to check friendship
    :rtype - obj if friendship exists, else false.
    """
    user_attr_val = ["sender_id", user_id]
    friend_attr_val = ["reciever_id", friend_id]
    friend_req = storage.get_by_double_field(
        Friend, user_attr_val, friend_attr_val
    )

    # It expect only one item from  filter
    for req in friend_req:
        return req
    return False



# ===================================================================== #
#                     Messages Module Helper Function                   #
# ===================================================================== #
def user_friend_messages(
    user_id: str, friend_id, is_reverse: bool = False
) -> Optional[PrivateMessage]:
    """
    Retrieve messages b/w logged-in user and friend(s),
    and sort the message base on time in ascendind order.

    :user_id - The logged-in user ID
    :friend_id - The friend ID

    :rtype - The sorted message if found, else None.
    """
    sender_attr_val = ["sender_id", user_id]
    reciever_attr_val = ["reciever_id", friend_id]
    messages = storage.get_by_double_field(
        PrivateMessage, sender_attr_val, reciever_attr_val
    )

    if not messages:
        return None

    sorted_messages = sorted(
        messages, key=lambda msg: msg.created_at, reverse=is_reverse
    )
    return sorted_messages


def user_messages(user_id: str) -> Optional[PrivateMessage]:
    """
    Retrieve all messages associated with logged-in user,
    and sort the message base on time in ascendind order.

    :user_id - The logged-in user ID

    :rtype - The sorted message if found, else None.
    """
    messages = (
        storage.get_by_field(PrivateMessage, "sender_id", user_id) +
        storage.get_by_field(PrivateMessage, "reciever_id", user_id)
    )
    if not user_messages:
        return None
    sorted_messages = sorted(
        messages, key=lambda msg: msg.created_at, reverse=True
    )
    return sorted_messages
