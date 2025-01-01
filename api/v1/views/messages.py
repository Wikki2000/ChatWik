#!/usr/bin/python3
"""Handle API views for message."""
from api.v1.views import api_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from models import storage
from models.private_message import PrivateMessage
from models.user import User
from api.v1.views.utils import user_friend_messages, user_messages



@api_views.route("/user-message-list", strict_slashes=False)
@jwt_required()
def msg_list():
    """Display recent message of logged-in user friend"""
    user_id = get_jwt_identity()
    users = storage.all(User).values()
    friends = []

    # Check for friends that has communication with logged-in user
    for friend in users:
        if user_friend_messages(user_id, friend.id):
            friends.append(friend)

    return jsonify([
        {
            "sender": {
                **friend.to_dict()
            },
            "message": [
                # Pick the most recent message object b/w user and friends
                msg.to_dict() for msg in user_friend_messages(
                    user_id, friend.id, is_reverse=True
                )][0]
        } for friend in friends
    ]), 200


@api_views.route(
    "/messages/<string:friend_id>/private-messages", strict_slashes=False
)
@swag_from("documentation/messages/get_message.yml")
@jwt_required()
def get_messages(friend_id):
    """
    Retrieve all private messages between the logged-in user and the receiver.
    Messages are sorted by timestamp (ascending order).
    """
    user_id = get_jwt_identity()

    sorted_messages = user_friend_messages(user_id, friend_id)

    if not sorted_messages:
        return jsonify([]), 200

    return jsonify([
        {
            "sender": {
                "first_name": msg.sender.first_name,
                "last_name": msg.sender.last_name,
                "username": msg.sender.username,
                "profile_photo": msg.sender.profile_photo,
                "sender_id": msg.sender.id
            },
            "reciever": {
                "first_name": msg.reciever.first_name,
                "last_name": msg.reciever.last_name,
                "username": msg.reciever.username,
                "profile_photo": msg.reciever.profile_photo,
                "reciever_id": msg.reciever.id
            },
            "message": {
                "content": msg.text,
                "timestamp": msg.created_at
            }
        } for msg in sorted_messages
    ]), 200
