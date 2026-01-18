from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..models import Conversation, ActionItem, Person
from ..schemas import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListResponse,
    ActionItemUpdate
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/", response_model=List[ConversationListResponse])
def get_conversations(
    skip: int = 0,
    limit: int = 100,
    person_id: Optional[str] = Query(None, description="Filter by person ID"),
    db: Session = Depends(get_db)
):
    """Get all conversations with optional filtering by person."""
    query = db.query(Conversation)

    if person_id:
        query = query.filter(Conversation.person_id == person_id)

    # Order by created_at descending (newest first)
    conversations = query.order_by(Conversation.created_at.desc()).offset(skip).limit(limit).all()

    # Transform to list response with action item count
    result = []
    for conv in conversations:
        active_count = sum(1 for item in conv.action_items if not item.completed)
        result.append(
            ConversationListResponse(
                id=conv.id,
                person_id=conv.person_id,
                participants=conv.participants or [],
                title=conv.title,
                date=conv.date,
                location=conv.location,
                summary=conv.summary,
                active_action_items_count=active_count
            )
        )

    return result


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific conversation by ID."""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )
    return conversation


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    # Verify person exists
    person = db.query(Person).filter(Person.id == conversation.person_id).first()
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {conversation.person_id} not found"
        )

    # Create conversation
    db_conversation = Conversation(
        person_id=conversation.person_id,
        participants=conversation.participants,
        title=conversation.title,
        date=conversation.date,
        location=conversation.location,
        summary=conversation.summary,
        key_points=conversation.key_points,
        full_transcript=conversation.full_transcript
    )
    db.add(db_conversation)
    db.flush()

    # Create action items
    for action_item_data in conversation.action_items:
        db_action_item = ActionItem(
            conversation_id=db_conversation.id,
            text=action_item_data.text,
            completed=action_item_data.completed
        )
        db.add(db_action_item)

    # Update person's met count and last met date
    person.met_count += 1
    person.last_met = conversation.date.split('•')[0].strip()

    db.commit()
    db.refresh(db_conversation)
    return db_conversation


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: str,
    conversation_update: ConversationUpdate,
    db: Session = Depends(get_db)
):
    """Update a conversation's information."""
    db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )

    update_data = conversation_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_conversation, field, value)

    db.commit()
    db.refresh(db_conversation)
    return db_conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a conversation."""
    db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found"
        )

    db.delete(db_conversation)
    db.commit()
    return None


@router.patch("/{conversation_id}/action-items/{item_id}", response_model=ConversationResponse)
def toggle_action_item(
    conversation_id: str,
    item_id: str,
    action_item_update: ActionItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an action item (typically to toggle completion status)."""
    db_action_item = db.query(ActionItem).filter(
        ActionItem.id == item_id,
        ActionItem.conversation_id == conversation_id
    ).first()

    if not db_action_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item with id {item_id} not found"
        )

    update_data = action_item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_action_item, field, value)

    db.commit()

    # Return the full conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    return conversation
