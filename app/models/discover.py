from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class DiscoverBatch(Base):
    __tablename__ = "discover_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    generated_for = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    candidates = relationship("DiscoverCandidate", back_populates="batch")

class DiscoverCandidate(Base):
    __tablename__ = "discover_candidates"

    batch_id = Column(UUID(as_uuid=True), ForeignKey("discover_batches.id", ondelete="CASCADE"), primary_key=True)
    candidate_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    rank = Column(Integer)
    reason = Column(String)

    # relationships
    batch = relationship("DiscoverBatch", back_populates="candidates")