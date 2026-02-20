from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserFilterPreference(Base):
    __tablename__ = "user_filter_preferences"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    filter_key = Column(String(50), primary_key=True)
    filter_values = Column(JSONB)
    allow_fallback = Column(Boolean, default=True)

    # relationships  
    user = relationship("User", back_populates="filter_preferences")