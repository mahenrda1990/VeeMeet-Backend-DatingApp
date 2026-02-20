from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class LikeResponse(BaseModel):
    status: str
    is_match: bool

class MatchResponse(BaseModel):
    match_id: UUID
    other_user_id: UUID
    created_at: datetime

class LikeHistoryResponse(BaseModel):
    liked_id: UUID
    created_at: datetime