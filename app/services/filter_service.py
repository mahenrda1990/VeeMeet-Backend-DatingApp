from sqlalchemy.orm import Session
from app.models.filter_preference import UserFilterPreference
import uuid

def set_filter_preference(db: Session, user_id: uuid.UUID, filter_key: str, filter_values: list, allow_fallback: bool = True):
    # Check if filter preference already exists
    existing_filter = db.query(UserFilterPreference).filter(
        UserFilterPreference.user_id == user_id,
        UserFilterPreference.filter_key == filter_key
    ).first()
    
    if existing_filter:
        # Update existing filter
        existing_filter.filter_values = filter_values
        existing_filter.allow_fallback = allow_fallback
        db.commit()
        db.refresh(existing_filter)
        return existing_filter
    else:
        # Create new filter preference
        new_filter = UserFilterPreference(
            user_id=user_id,
            filter_key=filter_key,
            filter_values=filter_values,
            allow_fallback=allow_fallback
        )
        db.add(new_filter)
        db.commit()
        db.refresh(new_filter)
        return new_filter

def get_user_filter_preferences(db: Session, user_id: uuid.UUID) -> list:
    preferences = db.query(UserFilterPreference).filter(
        UserFilterPreference.user_id == user_id
    ).all()
    
    return [{
        "filter_key": pref.filter_key,
        "filter_values": pref.filter_values,
        "allow_fallback": pref.allow_fallback
    } for pref in preferences]

def delete_filter_preference(db: Session, user_id: uuid.UUID, filter_key: str):
    preference = db.query(UserFilterPreference).filter(
        UserFilterPreference.user_id == user_id,
        UserFilterPreference.filter_key == filter_key
    ).first()
    
    if preference:
        db.delete(preference)
        db.commit()