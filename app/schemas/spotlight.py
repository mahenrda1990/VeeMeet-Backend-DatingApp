from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class DiscoverCandidateResponse(BaseModel):
    user_id: UUID
    first_name: Optional[str]
    gender: Optional[str]
    rank: int
    reason: str

class SpotlightSessionResponse(BaseModel):
    session_id: UUID
    started_at: datetime
    ends_at: datetime
    multiplier: float
    is_active: bool

class SpotlightBalanceResponse(BaseModel):
    balance: int

class SpotlightActivationRequest(BaseModel):
    duration_minutes: int = 30
    multiplier: float = 2.0