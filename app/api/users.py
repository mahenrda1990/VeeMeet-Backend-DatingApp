from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (alternative endpoint)"""
    return create_user(db, data)
