from sqlalchemy import Column, String, Integer, DateTime, ARRAY, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(String, primary_key=True, default=lambda: f"p{uuid.uuid4().hex[:8]}")
    name = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    avatar_color = Column(String, nullable=False, default="bg-indigo-200")
    context = Column(Text, nullable=False)
    interests = Column(ARRAY(String), default=list)
    open_follow_ups = Column(ARRAY(String), default=list)
    last_met = Column(String, nullable=True)
    met_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    conversations = relationship("Conversation", back_populates="primary_person")
