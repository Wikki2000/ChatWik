#!/usr/bin/python3
"""Handle API views for message.""" 
from api.v1.views import api_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from flask_socketio import SocketIO, emit, join_room
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.private_message import PrivateMessage
from models import storage
from typing import Any, Dict

# Create a SocketIO instance
socketio = SocketIO()


@socketio.on("send_message")
def send_msg(data: Dict[str, str]):
    """Event handler for sending a message."""
    verify_jwt_in_request()
    user_id = get_jwt_identity()

    # Save the message to the database
    msg: PrivateMessage = PrivateMessage(
        sender_id=user_id, 
        reciever_id=data.get("reciever_id"),
        text=data.get("message")
    )
    storage.new(msg)
    storage.save()

    # Add reciever name to data
    data['sender_name'] = msg.sender.username
    data['sender_id'] = user_id

    storage.close()

    room = create_room(data.get('reciever_id'), user_id)

    # Emit the message back to both sender and receiver
    emit('recieve_message', data, room=room)


@socketio.on("join_chat")
def join_chat(data: Dict[str, str]):
    """Join room for private chat."""
    # Manually apply jwt_required() logic for WebSockets
    verify_jwt_in_request()
    
    user_id = get_jwt_identity()
    room = create_room(user_id, data.get('reciever_id'))
    join_room(room)
    emit('success', {'message': 'Joined chat room'}, room=room)


def create_room(user_id_1: str, user_id_2: str) -> str:
    """
    Create a consistent room name based on the two user IDs,
    irrespective of their order.
    """
    if not user_id_1 or not user_id_2:
        raise ValueError("Both user IDs must be valid.")
    room = f"chat_{min(user_id_1, user_id_2)}_{max(user_id_1, user_id_2)}"
    return room
