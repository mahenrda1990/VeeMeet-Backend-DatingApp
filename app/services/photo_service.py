from sqlalchemy.orm import Session
from app.models.photo import ProfilePhoto
from fastapi import HTTPException
import uuid

def add_profile_photo(db: Session, user_id: uuid.UUID, photo_url: str, position: int) -> ProfilePhoto:
    # Check if position is already taken
    existing_photo = db.query(ProfilePhoto).filter(
        ProfilePhoto.user_id == user_id,
        ProfilePhoto.position == position
    ).first()
    
    if existing_photo:
        raise HTTPException(status_code=400, detail="Position already occupied")
    
    photo = ProfilePhoto(
        user_id=user_id,
        photo_url=photo_url,
        position=position
    )
    
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

def get_user_photos(db: Session, user_id: uuid.UUID) -> list:
    photos = db.query(ProfilePhoto).filter(
        ProfilePhoto.user_id == user_id
    ).order_by(ProfilePhoto.position).all()
    
    return photos

def delete_photo(db: Session, user_id: uuid.UUID, photo_id: uuid.UUID):
    photo = db.query(ProfilePhoto).filter(
        ProfilePhoto.id == photo_id,
        ProfilePhoto.user_id == user_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    db.delete(photo)
    db.commit()

def reorder_photos(db: Session, user_id: uuid.UUID, photo_positions: dict):
    """Reorder photos based on photo_id -> position mapping"""
    for photo_id, position in photo_positions.items():
        photo = db.query(ProfilePhoto).filter(
            ProfilePhoto.id == photo_id,
            ProfilePhoto.user_id == user_id
        ).first()
        
        if photo:
            photo.position = position
    
    db.commit()