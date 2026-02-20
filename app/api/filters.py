from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import SessionLocal
from app.schemas.filter import FilterPreferenceCreate, FilterPreferenceResponse
from app.services.filter_service import set_filter_preference, get_user_filter_preferences, delete_filter_preference

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

@router.get("/", response_model=List[FilterPreferenceResponse])
def get_filters(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's filter preferences"""
    preferences = get_user_filter_preferences(db, current_user_id)
    return [FilterPreferenceResponse(
        filter_key=pref["filter_key"],
        filter_values=pref["filter_values"],
        allow_fallback=pref["allow_fallback"]
    ) for pref in preferences]

@router.post("/")
def save_filter(filter_data: FilterPreferenceCreate, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Save or update a filter preference"""
    set_filter_preference(
        db, 
        current_user_id, 
        filter_data.filter_key, 
        filter_data.filter_values, 
        filter_data.allow_fallback
    )
    return {"message": "Filter saved"}

@router.delete("/{filter_key}")
def delete_filter(filter_key: str, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Delete a filter preference"""
    delete_filter_preference(db, current_user_id, filter_key)
    return {"message": "Filter deleted"}
