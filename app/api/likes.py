from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import SessionLocal
from app.schemas.like import LikeResponse, MatchResponse, LikeHistoryResponse
from app.services.like_service import like_user, get_user_likes, get_user_matches

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

@router.post("/{target_id}", response_model=LikeResponse)
def like(target_id: UUID, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Like another user"""
    result = like_user(db, current_user_id, target_id)
    return LikeResponse(status=result["status"], is_match=result["is_match"])

@router.get("/history", response_model=List[LikeHistoryResponse])
def get_like_history(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's like history"""
    likes = get_user_likes(db, current_user_id)
    return [LikeHistoryResponse(liked_id=like["liked_id"], created_at=like["created_at"]) for like in likes]

@router.get("/matches", response_model=List[MatchResponse])
def get_matches(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's matches"""
    matches = get_user_matches(db, current_user_id)
    return [MatchResponse(
        match_id=match["match_id"], 
        other_user_id=match["other_user_id"], 
        created_at=match["created_at"]
    ) for match in matches]
