#!/usr/bin/python3
"""This module models the storage of user details."""
from datetime import datetime
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Boolean
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base):
    """Define the class models for user."""
    __tablename__ = "users"
    name = Column(String(20), nullable=False)
    username = Column(String(20))
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(1500), nullable=False)
    is_active = Column(Boolean, default=False)

    def hash_password(self):
        """Hash password before storing in database."""
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        """Verify password and give access."""
        return check_password_hash(self.password, password)
