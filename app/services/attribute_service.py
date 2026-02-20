from sqlalchemy.orm import Session
from app.models.attribute import UserAttribute
from app.schemas.attribute import AttributeCreate
import uuid

def set_user_attribute(db: Session, user_id: uuid.UUID, attribute: AttributeCreate) -> UserAttribute:
    # Check if attribute already exists
    existing_attr = db.query(UserAttribute).filter(
        UserAttribute.user_id == user_id,
        UserAttribute.attribute_key == attribute.key
    ).first()
    
    if existing_attr:
        # Update existing attribute
        existing_attr.attribute_value = attribute.value
        db.commit()
        db.refresh(existing_attr)
        return existing_attr
    else:
        # Create new attribute
        new_attr = UserAttribute(
            user_id=user_id,
            attribute_key=attribute.key,
            attribute_value=attribute.value
        )
        db.add(new_attr)
        db.commit()
        db.refresh(new_attr)
        return new_attr

def get_user_attributes(db: Session, user_id: uuid.UUID) -> list:
    attributes = db.query(UserAttribute).filter(
        UserAttribute.user_id == user_id
    ).all()
    
    return [{"key": attr.attribute_key, "value": attr.attribute_value} for attr in attributes]

def delete_user_attribute(db: Session, user_id: uuid.UUID, attribute_key: str):
    attribute = db.query(UserAttribute).filter(
        UserAttribute.user_id == user_id,
        UserAttribute.attribute_key == attribute_key
    ).first()
    
    if attribute:
        db.delete(attribute)
        db.commit()