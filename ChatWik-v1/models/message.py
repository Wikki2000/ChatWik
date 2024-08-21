#!/usr/bin/python3
"""This module models the storage of user message."""
from models.base_model import Base, BaseModel
from datetime import datetime
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import Relationship


class Message(BaseModel, Base):
    """Define the class model for user messages."""
    __tablename__ = "messages"
    user_id = Column(String(50),  ForeignKey("users.id"), nullable=False)
    content = Column(String(600), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = Relationship("User", backref="messages")
