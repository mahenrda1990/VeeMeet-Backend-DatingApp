from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserResponse, PhoneLoginRequest
from app.services.user_service import create_user, authenticate_user, get_or_create_user_by_phone

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = create_user(db, user_data)
    return user

@router.post("/login", response_model=UserResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login user with email and password"""
    user = authenticate_user(db, login_data.email, login_data.password)
    return user

@router.post("/phone-login", response_model=UserResponse)
def phone_login(data: PhoneLoginRequest, db: Session = Depends(get_db)):
    """Called after Firebase OTP is successfully verified on the client.

    Creates the user if they don't exist yet, or returns the existing user.
    The `registration_step` in the response tells the client which
    onboarding screen to navigate to next:

        0  → Name + Birthday (first onboarding step)
        1  → Location
        2  → Gender
        3  → Gender visibility
        4  → Mode selection
        5  → Dating preferences
        6  → Dating intentions
        7  → Height
        8  → Interests
        9  → Lifestyle habits
        10 → Kids / family plans
        11 → Important values (religion / politics)
        12 → Add photos
        13 → Prompts
        14 → Complete → Home
    """
    user = get_or_create_user_by_phone(db, data.phone_number)
    return user
