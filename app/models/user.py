from sqlalchemy import Column, String, Date, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    first_name = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    profile_completion = Column(Integer, default=0)
    registration_step = Column(Integer, default=0)
    hide_name = Column(Boolean, default=False)
    snoozed_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Onboarding / profile fields
    gender_subs = Column(ARRAY(String))
    show_gender_on_profile = Column(Boolean, default=True)
    gender_visible_labels = Column(ARRAY(String))
    email_marketing_opt_in = Column(Boolean, default=False)
    mode = Column(String)
    dating_preferences = Column(ARRAY(String))
    open_to_everyone = Column(Boolean, default=False)
    dating_intentions = Column(ARRAY(String))
    height_cm = Column(Integer)
    interests = Column(ARRAY(String))
    drinking_habit = Column(String)
    smoking_habit = Column(String)
    have_kids = Column(String)
    kids_plan = Column(String)
    religion = Column(String)
    politics = Column(String)
    prompts = Column(ARRAY(String))
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    location_address = Column(String)
    
    # relationships
    photos = relationship("ProfilePhoto", back_populates="user")
    attributes = relationship("UserAttribute", back_populates="user")
    filter_preferences = relationship("UserFilterPreference", back_populates="user")
    spotlight = relationship("UserSpotlight", back_populates="user", uselist=False)
