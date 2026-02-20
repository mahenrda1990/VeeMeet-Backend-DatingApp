from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PhoneLoginRequest(BaseModel):
    """Called after Firebase OTP is verified on the client."""
    phone_number: str  # E.164 format, e.g. +919876543210

class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    hide_name: Optional[bool] = None
    # Onboarding / profile fields
    gender_subs: Optional[List[str]] = None
    show_gender_on_profile: Optional[bool] = None
    gender_visible_labels: Optional[List[str]] = None
    email_marketing_opt_in: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
    mode: Optional[str] = None
    dating_preferences: Optional[List[str]] = None
    open_to_everyone: Optional[bool] = None
    dating_intentions: Optional[List[str]] = None
    height_cm: Optional[int] = None
    interests: Optional[List[str]] = None
    drinking_habit: Optional[str] = None
    smoking_habit: Optional[str] = None
    have_kids: Optional[str] = None
    kids_plan: Optional[str] = None
    religion: Optional[str] = None
    politics: Optional[str] = None
    prompts: Optional[List[str]] = None
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    location_address: Optional[str] = None
    profile_completion: Optional[int] = None
    registration_step: Optional[int] = None

class RegistrationStepUpdate(BaseModel):
    registration_step: int

class UserResponse(BaseModel):
    id: UUID
    phone_number: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    profile_completion: int
    registration_step: int
    hide_name: bool
    created_at: datetime
    # Onboarding / profile summary (optional)
    show_gender_on_profile: Optional[bool] = None
    mode: Optional[str] = None
    dating_preferences: Optional[List[str]] = None
    dating_intentions: Optional[List[str]] = None
    height_cm: Optional[int] = None
    interests: Optional[List[str]] = None
    notifications_enabled: Optional[bool] = None
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    location_address: Optional[str] = None

    class Config:
        from_attributes = True

class ProfilePhotoResponse(BaseModel):
    id: UUID
    photo_url: str
    position: int
    created_at: datetime

    class Config:
        from_attributes = True

class AttributeResponse(BaseModel):
    key: str
    value: str

class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]
    profile_completion: int
    hide_name: bool
    photos: List[ProfilePhotoResponse]
    attributes: List[AttributeResponse]
    # Detailed onboarding / profile fields
    gender_subs: Optional[List[str]] = None
    show_gender_on_profile: Optional[bool] = None
    gender_visible_labels: Optional[List[str]] = None
    email_marketing_opt_in: Optional[bool] = None
    mode: Optional[str] = None
    dating_preferences: Optional[List[str]] = None
    open_to_everyone: Optional[bool] = None
    dating_intentions: Optional[List[str]] = None
    height_cm: Optional[int] = None
    interests: Optional[List[str]] = None
    drinking_habit: Optional[str] = None
    smoking_habit: Optional[str] = None
    have_kids: Optional[str] = None
    kids_plan: Optional[str] = None
    religion: Optional[str] = None
    politics: Optional[str] = None
    prompts: Optional[List[str]] = None
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    location_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
