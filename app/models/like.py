from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Like(Base):
    __tablename__ = "likes"

    liker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    liked_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
