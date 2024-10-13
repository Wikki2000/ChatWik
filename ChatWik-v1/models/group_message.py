#!/usr/bin/python3
"""This module models the storage of group chat by users."""
from models.base_model import Base, BaseModel
from datetime import datetime
from sqlalchemy import (
    Column, DateTime, String, Text, LargeBinary, ForeignKey
)


class GroupMessage(BaseModel, Base):
    """Define the class model for user messages."""
    __tablename__ = "group_messages"
    user_id = Column(
        String(50), 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    group_id = Column(
        String(50),
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False
    )
    text = Column(Text, nullable=False)
    media = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
