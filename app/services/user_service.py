from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException
import hashlib
import uuid

def create_user(db: Session, data: UserCreate) -> User:
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hashlib.sha256(data.password.encode()).hexdigest()

    user = User(
        email=data.email,
        password_hash=hashed,
        first_name=data.first_name,
        birth_date=data.birth_date,
        gender=data.gender
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

def get_user_by_id(db: Session, user_id: uuid.UUID) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if user.password_hash != hashed:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user

def get_or_create_user_by_phone(db: Session, phone_number: str) -> User:
    """Find user by phone number, or create a new one if not found."""
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user:
        return user

    user = User(phone_number=phone_number)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(db: Session, phone_number: str) -> User:
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_profile(db: Session, user_id: uuid.UUID, **kwargs) -> User:
    user = get_user_by_id(db, user_id)
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def update_registration_step(db: Session, user_id: uuid.UUID, step: int) -> User:
    user = get_user_by_id(db, user_id)
    user.registration_step = step
    db.commit()
    db.refresh(user)
    return user