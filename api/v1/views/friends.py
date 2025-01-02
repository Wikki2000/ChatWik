#!/usr/bin/python3
"""Handle CRUD operation for Friend model.
"""
from models.friend import Friend
from models.user import User
from models import storage
from flask import jsonify
from api.v1.views import api_views
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from api.v1.views.utils import friendship, is_friend, user_friend_messages


@api_views.route("/friends-request")
@jwt_required()
def friends_request():
    """Retrieve friend requests sent to user."""
    user_id = get_jwt_identity()
    requests = storage.get_by_field(Friend, "reciever_id", user_id)
    if not requests:
        return jsonify([]), 200

    friends_req = [
        req.sender.to_dict() for req in requests if not req.is_friend
    ]
    return jsonify(friends_req), 200


@api_views.route("/friends")
@jwt_required()
def friends():
    """Retrieve user friends who has accepted his request.
    """
    user_id = get_jwt_identity()
    friends_obj = storage.all(User).values()
    if not friends_obj:
        return jsonify([]), 200

    friends = [
        friend.to_dict() for friend in friends_obj
        if is_friend(user_id, friend.id)
    ]
    return jsonify(friends), 200


@api_views.route("/friends-suggestion")
@jwt_required()
def friends_suggestion():
    """
    Suggest friends in the same state as the user,
    and excluding current friends.
    """
    user_id = get_jwt_identity()
    user = storage.get_by_id(User, user_id)

    # Get all users in the same state as the current user
    friends_in_same_state = storage.get_by_field(User, "state", user.state)
    if not friends_in_same_state:
        return jsonify([]), 200

    # List to collect suggested friends who are not current friends
    not_friends = []

    for friend in friends_in_same_state:
        # Skip the current user
        if friend.id == user_id:
            continue

        # Check if there’s no friendship,
        if not is_friend(user_id, friend.id):
            not_friends.append(friend)

    # Build the response list
    friends_list = [
        {
            **friend.to_dict(),
            "is_sent": any(
                req.sender_id == user_id for req in friend.recieve_request
            )
        }
        for friend in not_friends
        # Skip if the friend has already sent a request to the current user
        if not any(
            friendship(user_id, friend.id) for req in friend.send_request
        )
    ]
    return jsonify(friends_list), 200


@api_views.route("/friends/<string:friend_id>/sent-request", methods=["POST"])
@jwt_required()
def friend_request(friend_id):
    """Send friendship request
    """
    user_id = get_jwt_identity()

    user_list = ["sender_id", user_id]
    friend_list = ["reciever_id", friend_id]
    if storage.get_by_double_field(Friend, user_list, friend_list):
        return jsonify({"error": "Friendship Already Exists"}), 409

    try:
        friend_req = Friend(sender_id=user_id, reciever_id=friend_id)
        storage.new(friend_req)
        storage.save()
        return jsonify({"status": "Friend Request sent"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": "Internal Error"}), 500


@api_views.route("/friends/<string:friend_id>/accept-request", methods=["PUT"])
@jwt_required()
def accept_friends(friend_id):
    """Accept friends request by user
    """
    user_id = get_jwt_identity()
    friend_req = friendship(user_id, friend_id)
    if not friend_req:
        return jsonify({"error": "No Friendship Record Found"}), 404
    friend_req.is_friend = True
    storage.save()
    storage.close()
    return jsonify({
        "status": "Success", "msg": "Friend Request Accepted"
    }), 200


@api_views.route(
    "/friends/<string:friend_id>/cancel-request", methods=["DELETE"]
)
@jwt_required()
def cancel_request(friend_id):
    """
    """
    user_id = get_jwt_identity()
    req = friendship(user_id, friend_id)
    if not req:
        abort(404)
    storage.delete(req)
    storage.save()
    storage.close()
    return jsonify({
        "status": "Success",
        "msg": "Delete Successfull"
    }), 200
