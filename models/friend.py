#!/usr/bin/python3
"""This modules manage the freinds of users."""
from models.base_model import Base, BaseModel
from datetime import datetime
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import Relationship


class Friend(BaseModel, Base):
    """Define the class model for users freinds."""
    __tablename__ = "friends"
    sender_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    reciever_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    is_friend = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
