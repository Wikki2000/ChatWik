#!/usr/bin/python3
"""This module models the storage of user details."""
from datetime import datetime
from models.base_model import Base, BaseModel
from models.group_message import GroupMessage
from models.private_message import PrivateMessage
from models.enrollment import Enrollment
from models.group import Group
from sqlalchemy import Column, String, Boolean, LargeBinary
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
    password = Column(String(1500), nullable=False)
    is_active = Column(Boolean, default=False)

    # Define relationship with other class
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
    groups = relationship("Group", secondary="enrollments", backref="users") 
    group_messages = relationship(
            "GroupMessage", backref="user",
            cascade="all, delete-orphan"
    )

    # ===================== Method Definition ==================== #
    def hash_password(self):
        """Hash password before storing in database."""
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        """Verify password and give access."""
        return check_password_hash(self.password, password)
