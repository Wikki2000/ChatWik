#!/usr/bin/python3
"""Stores Group Created by Users"""
from models.base_model import Base, BaseModel
from models.private_message import PrivateMessage
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship


class Group(BaseModel, Base):
    """Define the class model for users created group."""
    __tablename__ = "groups"
    name = Column(String(50), nullable=False)
    description = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    group_messages = relationship(
        "GroupMessage",
        cascade="all, delete-orphan",
        backref="group"
    )
