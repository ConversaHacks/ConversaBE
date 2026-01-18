from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models import Person
from ..schemas import PersonCreate, PersonUpdate, PersonResponse, PersonListResponse

router = APIRouter(prefix="/people", tags=["people"])


@router.get("/", response_model=List[PersonListResponse])
def get_people(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all people."""
    people = db.query(Person).offset(skip).limit(limit).all()
    return people


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(
    person_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific person by ID."""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )
    return person


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db)
):
    """Create a new person."""
    db_person = Person(
        name=person.name,
        role=person.role,
        avatar_color=person.avatar_color,
        context=person.context,
        interests=person.interests,
        open_follow_ups=person.open_follow_ups
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


@router.put("/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: str,
    person_update: PersonUpdate,
    db: Session = Depends(get_db)
):
    """Update a person's information."""
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )

    update_data = person_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_person, field, value)

    db.commit()
    db.refresh(db_person)
    return db_person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: str,
    db: Session = Depends(get_db)
):
    """Delete a person."""
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found"
        )

    db.delete(db_person)
    db.commit()
    return None
