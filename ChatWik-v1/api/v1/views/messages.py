#!/usr/bin/python3
"""Handle API views for message."""
from api.v1.views import api_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from models import storage
from models.private_message import PrivateMessage
from sqlalchemy import or_


@api_views.route(
    "/receiver/<string:receiver_id>/private-messages", strict_slashes=False
)
@swag_from("documentation/messages/get_message.yml")
@jwt_required()
def get_messages(receiver_id):
    """
    Retrieve all private messages between the logged-in user and the receiver.
    Messages are sorted by timestamp (ascending order).
    """
    session = storage.get_session()
    sender_id = get_jwt_identity()

    # Retrieve all messages between the sender and receiver, ordered by timestamp
    messages = session.query(PrivateMessage).filter(
        or_(
            (PrivateMessage.sender_id == sender_id) & (PrivateMessage.reciever_id == receiver_id),
            (PrivateMessage.sender_id == receiver_id) & (PrivateMessage.reciever_id == sender_id)
        )
    ).order_by(PrivateMessage.created_at.asc()).all()

    # If no messages found, return 404
    if not messages:
        abort(404)

    return jsonify([
        {
            "sender": {
                "first_name": msg.sender.first_name,
                "last_name": msg.sender.last_name,
                "username": msg.sender.username,
                "profile_photo": msg.sender.profile_photo,
                "sender_id": msg.sender.id
            },
            "receiver": {
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
        } for msg in messages
    ]), 200
