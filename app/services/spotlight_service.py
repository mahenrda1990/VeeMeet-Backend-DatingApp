from sqlalchemy.orm import Session
from app.models.spotlight import UserSpotlight, SpotlightSession
from datetime import datetime, timedelta
from fastapi import HTTPException
import uuid

def get_user_spotlight(db: Session, user_id: uuid.UUID) -> UserSpotlight:
    spotlight = db.query(UserSpotlight).filter(
        UserSpotlight.user_id == user_id
    ).first()
    
    if not spotlight:
        # Create spotlight entry if it doesn't exist
        spotlight = UserSpotlight(user_id=user_id, balance=0)
        db.add(spotlight)
        db.commit()
        db.refresh(spotlight)
    
    return spotlight

def add_spotlight_balance(db: Session, user_id: uuid.UUID, amount: int) -> UserSpotlight:
    spotlight = get_user_spotlight(db, user_id)
    spotlight.balance += amount
    db.commit()
    db.refresh(spotlight)
    return spotlight

def activate_spotlight(db: Session, user_id: uuid.UUID, duration_minutes: int = 30, multiplier: float = 2.0) -> SpotlightSession:
    spotlight = get_user_spotlight(db, user_id)
    
    # Check if user has balance
    cost = 1  # 1 spotlight credit per activation
    if spotlight.balance < cost:
        raise HTTPException(status_code=400, detail="Insufficient spotlight balance")
    
    # Check if user already has an active session
    active_session = db.query(SpotlightSession).filter(
        SpotlightSession.user_id == user_id,
        SpotlightSession.ends_at > datetime.utcnow()
    ).first()
    
    if active_session:
        raise HTTPException(status_code=400, detail="Spotlight session already active")
    
    # Deduct from balance
    spotlight.balance -= cost
    
    # Create new session
    now = datetime.utcnow()
    session = SpotlightSession(
        user_id=user_id,
        started_at=now,
        ends_at=now + timedelta(minutes=duration_minutes),
        multiplier=multiplier
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_active_spotlight_session(db: Session, user_id: uuid.UUID) -> SpotlightSession:
    session = db.query(SpotlightSession).filter(
        SpotlightSession.user_id == user_id,
        SpotlightSession.ends_at > datetime.utcnow()
    ).first()
    
    return session

def get_spotlight_history(db: Session, user_id: uuid.UUID) -> list:
    sessions = db.query(SpotlightSession).filter(
        SpotlightSession.user_id == user_id
    ).order_by(SpotlightSession.started_at.desc()).all()
    
    return [{
        "session_id": session.id,
        "started_at": session.started_at,
        "ends_at": session.ends_at,
        "multiplier": session.multiplier,
        "is_active": session.ends_at > datetime.utcnow()
    } for session in sessions]