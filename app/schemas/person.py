from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PersonBase(BaseModel):
    name: str
    role: str
    avatar_color: str = Field(..., description="Tailwind color class for avatar")
    context: str = Field(..., description="Context about how you met or know this person")
    interests: List[str] = Field(default_factory=list)
    open_follow_ups: List[str] = Field(default_factory=list)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    avatar_color: Optional[str] = None
    context: Optional[str] = None
    interests: Optional[List[str]] = None
    open_follow_ups: Optional[List[str]] = None


class PersonResponse(PersonBase):
    id: str
    last_met: Optional[str] = None
    met_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PersonListResponse(BaseModel):
    id: str
    name: str
    role: str
    avatar_color: str
    last_met: Optional[str] = None
    met_count: int
    context: str

    class Config:
        from_attributes = True
