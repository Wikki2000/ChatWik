#!/usr/bin/python3
"""Enroll Users in a Group."""
from models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy import Column, DateTime, String, ForeignKey


class Enrollment(Base):
    """Define class for user enrollment in a group."""
    __tablename__ = "enrollments"
    group_id = Column(
        String(50),
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False) 
