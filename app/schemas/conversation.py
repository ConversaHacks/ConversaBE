from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ActionItemBase(BaseModel):
    text: str
    completed: bool = False


class ActionItemCreate(ActionItemBase):
    pass


class ActionItemUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None


class ActionItemResponse(ActionItemBase):
    id: str

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    title: str
    date: str = Field(..., description="Formatted date string (e.g., 'Jan 16 • 2:30 PM')")
    location: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    full_transcript: Optional[str] = None


class ConversationCreate(ConversationBase):
    person_id: str
    participants: List[str] = Field(default_factory=list, description="List of participant IDs")
    action_items: List[ActionItemCreate] = Field(default_factory=list)


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    full_transcript: Optional[str] = None
    person_id: Optional[str] = None
    participants: Optional[List[str]] = None


class ConversationResponse(ConversationBase):
    id: str
    person_id: str
    participants: List[str]
    action_items: List[ActionItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    id: str
    person_id: str
    participants: List[str]
    title: str
    date: str
    location: str
    summary: str
    active_action_items_count: int

    class Config:
        from_attributes = True
