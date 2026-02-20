from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import SessionLocal
from app.schemas.spotlight import (
    SpotlightBalanceResponse, 
    SpotlightSessionResponse, 
    SpotlightActivationRequest
)
from app.services.spotlight_service import (
    get_user_spotlight, 
    activate_spotlight, 
    get_active_spotlight_session, 
    get_spotlight_history,
    add_spotlight_balance
)

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

@router.get("/balance", response_model=SpotlightBalanceResponse)
def get_balance(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's spotlight balance"""
    spotlight = get_user_spotlight(db, current_user_id)
    return SpotlightBalanceResponse(balance=spotlight.balance)

@router.post("/activate", response_model=SpotlightSessionResponse)
def activate(
    activation_data: SpotlightActivationRequest,
    db: Session = Depends(get_db), 
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Activate spotlight for the current user"""
    session = activate_spotlight(
        db, 
        current_user_id, 
        activation_data.duration_minutes, 
        activation_data.multiplier
    )
    return SpotlightSessionResponse(
        session_id=session.id,
        started_at=session.started_at,
        ends_at=session.ends_at,
        multiplier=session.multiplier,
        is_active=True
    )

@router.get("/active")
def get_active_session(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's active spotlight session"""
    session = get_active_spotlight_session(db, current_user_id)
    if not session:
        return {"message": "No active spotlight session"}
    
    return SpotlightSessionResponse(
        session_id=session.id,
        started_at=session.started_at,
        ends_at=session.ends_at,
        multiplier=session.multiplier,
        is_active=True
    )

@router.get("/history", response_model=List[SpotlightSessionResponse])
def get_history(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's spotlight session history"""
    history = get_spotlight_history(db, current_user_id)
    return [SpotlightSessionResponse(
        session_id=session["session_id"],
        started_at=session["started_at"],
        ends_at=session["ends_at"],
        multiplier=session["multiplier"],
        is_active=session["is_active"]
    ) for session in history]

@router.post("/add-balance/{amount}")
def add_balance(amount: int, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Add spotlight balance (for testing/admin purposes)"""
    spotlight = add_spotlight_balance(db, current_user_id, amount)
    return {"message": f"Added {amount} spotlight credits", "new_balance": spotlight.balance}
