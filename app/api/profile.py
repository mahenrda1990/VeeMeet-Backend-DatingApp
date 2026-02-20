from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from app.core.database import SessionLocal
from app.schemas.user import UserUpdate, UserProfileResponse, ProfilePhotoResponse, RegistrationStepUpdate
from app.schemas.attribute import AttributeCreate, AttributeResponse
from app.schemas.photo import PhotoCreate, PhotoReorder
from app.services.user_service import get_user_by_id, update_user_profile, update_registration_step
from app.services.attribute_service import set_user_attribute, get_user_attributes, delete_user_attribute
from app.services.photo_service import add_profile_photo, get_user_photos, delete_photo, reorder_photos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> UUID:
    """Read user ID from the X-User-Id header (temporary until JWT auth is added)."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-Id header is required")
    try:
        return UUID(x_user_id)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid X-User-Id header")

@router.get("/me", response_model=UserProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's full profile"""
    user = get_user_by_id(db, current_user_id)
    photos = get_user_photos(db, current_user_id)
    attributes = get_user_attributes(db, current_user_id)
    
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        birth_date=user.birth_date,
        gender=user.gender,
        profile_completion=user.profile_completion,
        hide_name=user.hide_name,
         gender_subs=user.gender_subs,
         show_gender_on_profile=user.show_gender_on_profile,
         gender_visible_labels=user.gender_visible_labels,
         email_marketing_opt_in=user.email_marketing_opt_in,
         mode=user.mode,
         dating_preferences=user.dating_preferences,
         open_to_everyone=user.open_to_everyone,
         dating_intentions=user.dating_intentions,
         height_cm=user.height_cm,
         interests=user.interests,
         drinking_habit=user.drinking_habit,
         smoking_habit=user.smoking_habit,
         have_kids=user.have_kids,
         kids_plan=user.kids_plan,
         religion=user.religion,
         politics=user.politics,
         prompts=user.prompts,
         location_latitude=user.location_latitude,
         location_longitude=user.location_longitude,
         location_address=user.location_address,
        photos=[ProfilePhotoResponse(
            id=photo.id,
            photo_url=photo.photo_url,
            position=photo.position,
            created_at=photo.created_at
        ) for photo in photos],
        attributes=[AttributeResponse(
            key=attr["key"],
            value=attr["value"]
        ) for attr in attributes],
        created_at=user.created_at
    )

@router.put("/me")
def update_profile(profile_data: UserUpdate, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Update current user's profile (any subset of fields)"""
    user = update_user_profile(
        db,
        current_user_id,
        **{k: v for k, v in profile_data.model_dump(exclude_none=True).items()}
    )
    return {"message": "Profile updated", "user_id": str(user.id)}

@router.patch("/registration-step")
def set_registration_step(data: RegistrationStepUpdate, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Update the current user's registration step.

    Call this after each onboarding screen is completed so the server knows
    where to resume if the user drops off and comes back.
    """
    user = update_registration_step(db, current_user_id, data.registration_step)
    return {"registration_step": user.registration_step}

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(user_id: UUID, db: Session = Depends(get_db)):
    """Get another user's profile (public view)"""
    user = get_user_by_id(db, user_id)
    photos = get_user_photos(db, user_id)
    attributes = get_user_attributes(db, user_id)
    
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name if not user.hide_name else None,
        birth_date=user.birth_date,
        gender=user.gender,
        profile_completion=user.profile_completion,
        hide_name=user.hide_name,
         gender_subs=user.gender_subs,
         show_gender_on_profile=user.show_gender_on_profile,
         gender_visible_labels=user.gender_visible_labels,
         email_marketing_opt_in=user.email_marketing_opt_in,
         mode=user.mode,
         dating_preferences=user.dating_preferences,
         open_to_everyone=user.open_to_everyone,
         dating_intentions=user.dating_intentions,
         height_cm=user.height_cm,
         interests=user.interests,
         drinking_habit=user.drinking_habit,
         smoking_habit=user.smoking_habit,
         have_kids=user.have_kids,
         kids_plan=user.kids_plan,
         religion=user.religion,
         politics=user.politics,
         prompts=user.prompts,
         location_latitude=user.location_latitude,
         location_longitude=user.location_longitude,
         location_address=user.location_address,
        photos=[ProfilePhotoResponse(
            id=photo.id,
            photo_url=photo.photo_url,
            position=photo.position,
            created_at=photo.created_at
        ) for photo in photos],
        attributes=[AttributeResponse(
            key=attr["key"],
            value=attr["value"]
        ) for attr in attributes],
        created_at=user.created_at
    )

# Photo endpoints
@router.post("/photos", response_model=ProfilePhotoResponse)
def add_photo(photo_data: PhotoCreate, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Add a new profile photo"""
    photo = add_profile_photo(db, current_user_id, photo_data.photo_url, photo_data.position)
    return ProfilePhotoResponse(
        id=photo.id,
        photo_url=photo.photo_url,
        position=photo.position,
        created_at=photo.created_at
    )

@router.get("/photos", response_model=List[ProfilePhotoResponse])
def get_photos(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's photos"""
    photos = get_user_photos(db, current_user_id)
    return [ProfilePhotoResponse(
        id=photo.id,
        photo_url=photo.photo_url,
        position=photo.position,
        created_at=photo.created_at
    ) for photo in photos]

@router.delete("/photos/{photo_id}")
def remove_photo(photo_id: UUID, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Delete a profile photo"""
    delete_photo(db, current_user_id, photo_id)
    return {"message": "Photo deleted"}

@router.put("/photos/reorder")
def reorder_profile_photos(reorder_data: PhotoReorder, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Reorder profile photos"""
    reorder_photos(db, current_user_id, reorder_data.photo_positions)
    return {"message": "Photos reordered"}

# Attribute endpoints
@router.post("/attributes")
def add_attribute(attribute: AttributeCreate, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Add or update a user attribute"""
    set_user_attribute(db, current_user_id, attribute)
    return {"message": "Attribute saved"}

@router.get("/attributes", response_model=List[AttributeResponse])
def get_attributes(db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Get current user's attributes"""
    attributes = get_user_attributes(db, current_user_id)
    return [AttributeResponse(key=attr["key"], value=attr["value"]) for attr in attributes]

@router.delete("/attributes/{attribute_key}")
def remove_attribute(attribute_key: str, db: Session = Depends(get_db), current_user_id: UUID = Depends(get_current_user_id)):
    """Delete a user attribute"""
    delete_user_attribute(db, current_user_id, attribute_key)
    return {"message": "Attribute deleted"}
