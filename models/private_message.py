#!/usr/bin/python3
"""This module models the storage of users message."""
from models.base_model import Base, BaseModel
from datetime import datetime
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, LargeBinary, Boolean
)
from sqlalchemy.orm import Relationship


class PrivateMessage(BaseModel, Base):
    """Define the class model for messages b/w two users."""
    __tablename__ = "private_messages"
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
    text = Column(String(600))
    media = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_read = Column(Boolean, default=False)
