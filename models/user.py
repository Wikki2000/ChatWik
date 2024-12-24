#!/usr/bin/python3
"""This module models the storage of user details."""
from datetime import datetime
from models.base_model import Base, BaseModel
from models.friend import Friend
#from models.group_message import GroupMessage
from models.private_message import PrivateMessage
#from models.enrollment import Enrollment
#from models.group import Group
from sqlalchemy import Column, String, Boolean, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base):
    """Define the class models for user."""
    __tablename__ = "users"
    first_name = Column(String(20), nullable=False)
    last_name =  Column(String(20), nullable=False)
    username = Column(String(20))
    profile_photo = Column(LargeBinary)
    email = Column(String(30), nullable=False, unique=True)
    state = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)
    password = Column(String(1500), nullable=False)
    is_active = Column(Boolean, default=False)
    last_active = Column(DateTime)

    # ========= Define relationship with other class ======== #
    # Define relationship with Friend class
    send_request = relationship(
        "Friend", backref="sender",
        cascade="all, delete-orphan",
        foreign_keys="Friend.sender_id"
    )
    recieve_request = relationship(
        "Friend", backref="reciever",
        cascade="all, delete-orphan",
        foreign_keys="Friend.reciever_id"
    )

    # Define relationship with Message class
    sent_messages = relationship(
        "PrivateMessage", backref="sender",
        cascade="all, delete-orphan",
        foreign_keys="PrivateMessage.sender_id"
    )
    recieved_messages = relationship(
        "PrivateMessage", backref="reciever",
        cascade="all, delete-orphan",
        foreign_keys="PrivateMessage.reciever_id"
    )
    """
    groups = relationship("Group", secondary="enrollments", backref="users") 
    group_messages = relationship(
            "GroupMessage", backref="user",
            cascade="all, delete-orphan"
    )
    """

    # ===================== Method Definition ==================== #
    def hash_password(self):
        """Hash password before storing in database."""
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        """Verify password and give access."""
        return check_password_hash(self.password, password)
