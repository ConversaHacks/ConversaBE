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
    face_embedding: Optional[List[str]] = None
    face_thumbnail_base64: Optional[str] = None
    physical_description: Optional[str] = None


class PersonUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    avatar_color: Optional[str] = None
    context: Optional[str] = None
    interests: Optional[List[str]] = None
    open_follow_ups: Optional[List[str]] = None
    face_embedding: Optional[List[str]] = None
    face_thumbnail_base64: Optional[str] = None
    physical_description: Optional[str] = None


class PersonResponse(PersonBase):
    id: str
    last_met: Optional[str] = None
    met_count: int = 0
    physical_description: Optional[str] = None
    has_face_data: bool = False
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
    has_face_data: bool = False

    class Config:
        from_attributes = True


class FaceMatchRequest(BaseModel):
    """Request to match a face embedding against known people."""
    face_embedding: List[str] = Field(..., description="Face embedding as list of float strings")
    threshold: float = Field(default=0.6, description="Similarity threshold (0-1)")


class FaceMatchResponse(BaseModel):
    """Response from face matching."""
    matched: bool
    person_id: Optional[str] = None
    person_name: Optional[str] = None
    confidence: float = 0.0
