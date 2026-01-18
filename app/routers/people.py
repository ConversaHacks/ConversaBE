from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import base64
import math

from ..core.database import get_db
from ..models import Person
from ..schemas import PersonCreate, PersonUpdate, PersonResponse, PersonListResponse, FaceMatchRequest, FaceMatchResponse

router = APIRouter(prefix="/people", tags=["people"])


def cosine_similarity(embedding1: List[str], embedding2: List[str]) -> float:
    """Calculate cosine similarity between two embeddings."""
    if not embedding1 or not embedding2 or len(embedding1) != len(embedding2):
        return 0.0

    vec1 = [float(x) for x in embedding1]
    vec2 = [float(x) for x in embedding2]

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


@router.get("/", response_model=List[PersonListResponse])
def get_people(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all people."""
    people = db.query(Person).offset(skip).limit(limit).all()
    # Add has_face_data field
    result = []
    for p in people:
        person_dict = {
            "id": p.id,
            "name": p.name,
            "role": p.role,
            "avatar_color": p.avatar_color,
            "last_met": p.last_met,
            "met_count": p.met_count,
            "context": p.context,
            "has_face_data": p.face_embedding is not None and len(p.face_embedding) > 0
        }
        result.append(person_dict)
    return result


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
    # Add has_face_data field
    result = PersonResponse.model_validate(person)
    result.has_face_data = person.face_embedding is not None and len(person.face_embedding) > 0
    return result


@router.post("/match-face", response_model=FaceMatchResponse)
def match_face(
    request: FaceMatchRequest,
    db: Session = Depends(get_db)
):
    """Match a face embedding against known people."""
    # Get all people with face embeddings
    people_with_faces = db.query(Person).filter(Person.face_embedding.isnot(None)).all()

    best_match = None
    best_similarity = 0.0

    for person in people_with_faces:
        if person.face_embedding:
            similarity = cosine_similarity(request.face_embedding, person.face_embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = person

    if best_match and best_similarity >= request.threshold:
        return FaceMatchResponse(
            matched=True,
            person_id=best_match.id,
            person_name=best_match.name,
            confidence=best_similarity
        )

    return FaceMatchResponse(matched=False, confidence=best_similarity)


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db)
):
    """Create a new person."""
    # Handle face thumbnail if provided
    face_thumbnail = None
    if person.face_thumbnail_base64:
        face_thumbnail = base64.b64decode(person.face_thumbnail_base64)

    db_person = Person(
        name=person.name,
        role=person.role,
        avatar_color=person.avatar_color,
        context=person.context,
        interests=person.interests,
        open_follow_ups=person.open_follow_ups,
        face_embedding=person.face_embedding,
        face_thumbnail=face_thumbnail,
        physical_description=person.physical_description
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

    result = PersonResponse.model_validate(db_person)
    result.has_face_data = db_person.face_embedding is not None and len(db_person.face_embedding) > 0
    return result


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

    # Handle face thumbnail separately
    if "face_thumbnail_base64" in update_data:
        thumbnail_b64 = update_data.pop("face_thumbnail_base64")
        if thumbnail_b64:
            db_person.face_thumbnail = base64.b64decode(thumbnail_b64)

    for field, value in update_data.items():
        setattr(db_person, field, value)

    db.commit()
    db.refresh(db_person)

    result = PersonResponse.model_validate(db_person)
    result.has_face_data = db_person.face_embedding is not None and len(db_person.face_embedding) > 0
    return result


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
