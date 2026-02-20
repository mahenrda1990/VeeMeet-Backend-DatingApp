from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from datetime import date
from app.core.database import SessionLocal
from app.schemas.spotlight import DiscoverCandidateResponse
from app.services.discover_service import get_discover_candidates

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: Replace with proper authentication middleware
def get_current_user_id() -> UUID:
    # This is temporary - should be replaced with proper JWT authentication
    return UUID("00000000-0000-0000-0000-000000000001")

@router.get("/", response_model=List[DiscoverCandidateResponse])
def discover(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get daily discover candidates for the current user"""
    candidates = get_discover_candidates(db, current_user_id)
    return [DiscoverCandidateResponse(
        user_id=candidate["user_id"],
        first_name=candidate["first_name"],
        gender=candidate["gender"],
        rank=candidate["rank"],
        reason=candidate["reason"]
    ) for candidate in candidates]

@router.get("/{target_date}", response_model=List[DiscoverCandidateResponse])
def discover_by_date(target_date: date, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get discover candidates for a specific date"""
    candidates = get_discover_candidates(db, current_user_id, target_date)
    return [DiscoverCandidateResponse(
        user_id=candidate["user_id"],
        first_name=candidate["first_name"],
        gender=candidate["gender"],
        rank=candidate["rank"],
        reason=candidate["reason"]
    ) for candidate in candidates]
