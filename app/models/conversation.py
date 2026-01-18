from sqlalchemy import Column, String, DateTime, ARRAY, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: f"c{uuid.uuid4().hex[:8]}")
    person_id = Column(String, ForeignKey("people.id"), nullable=False, index=True)
    participants = Column(ARRAY(String), default=list)
    title = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    key_points = Column(ARRAY(String), default=list)
    full_transcript = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    primary_person = relationship("Person", back_populates="conversations")
    action_items = relationship("ActionItem", back_populates="conversation", cascade="all, delete-orphan")


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(String, primary_key=True, default=lambda: f"a{uuid.uuid4().hex[:8]}")
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="action_items")
