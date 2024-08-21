#!/usr/bin/python3
"""Handle API views for message.""" 
from api.v1.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.message import Message


@app_views.route("/messages", strict_slashes=False)
#@jwt_required()
def get_messages():
    """
    Retrieve all messages and it coressponding users.
    This message object are sorted with respest to timestamp.
    """
    messages = storage.all(Message).values()
    sort_messages = sorted(messages, key=lambda msg: msg.timestamp)
    msg_list = [
            {
                "id": message.id, "created_by": message.user.name,
                "created_at": message.timestamp, "content": message.content
            } for message in sort_messages
    ]
    return jsonify(msg_list)


@app_views.route("/messages/<mesg_id>", methods=["DELETE"], strict_slashes=False)
def del_messages(mesg_id):
    """Handle view for message deletion."""
    messages = storage.all(Message)
    key = "Message." + mesg_id
    message = messages.get(key)
    if not message:
        abort(404)
    storage.delete(message)
    storage.save()
    return jsonify({
        "status": "Success", 
        "message": "Message Deleted Successfully"
        }), 200


@app_views.route("/messages/<mesg_id>", methods=["PUT"], strict_slashes=False)
def put_messages(mesg_id):
    """Handle view for updating message."""
    data = request.get_json()
    if not data:
        abort(400, "Not a valid JSON")

    messages = storage.all(Message)
    key = "Message." + mesg_id
    message = messages.get(key)
    if not message:
        abort(404)

    # User should only be allow to update msg cintent..
    ignored_field = ["id", "timestamp", "user_id"]
    for key, value in data.items():
        if key not in ignored_field:
            setattr(message, key, value)
    storage.save()
    return jsonify({
        "id": message.id,
        "content": message.content,
        "user_id": message.user_id,
        "timestamp": message.timestamp
        }), 200


@app_views.route("/messages", methods=["POST"])
#@jwt_required()
def post_message():
    """This endpoint handle view for creation of message."""
    data = request.get_json()
    user_id = get_jwt_identity()

    # Handle 400 error
    if not data:
        error = {"status": "Bad Request", "message": "Empty Request Body"}
        return jsonify(error), 400
    elif not data.get("content"):
        error = {"status": "Bad Request", "message": "content field missing"}
        return jsonify(error), 400

    # Create message
    message = Message(user_id=user_id, content=data.get("content"))
    storage.new(message)
    storage.save()
    return jsonify({
        "id": message.id,
        "content": message.content,
        "username": message.user.name,
        "user_id": message.user_id,
        "timestamp": message.timestamp
        }), 201
