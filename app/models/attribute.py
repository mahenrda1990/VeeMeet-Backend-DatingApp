from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserAttribute(Base):
    __tablename__ = "user_attributes"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    attribute_key = Column(String(50), primary_key=True)
    attribute_value = Column(String(100))

    # relationships
    user = relationship("User", back_populates="attributes")
