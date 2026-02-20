from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class UserSpotlight(Base):
    __tablename__ = "user_spotlights"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    balance = Column(Integer, default=0)

    # relationships
    user = relationship("User", back_populates="spotlight")
    sessions = relationship("SpotlightSession", back_populates="spotlight")

class SpotlightSession(Base):
    __tablename__ = "spotlight_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_spotlights.user_id"))
    started_at = Column(DateTime(timezone=True))
    ends_at = Column(DateTime(timezone=True))
    multiplier = Column(Float, default=1.0)

    # relationships
    spotlight = relationship("UserSpotlight", back_populates="sessions")