from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PhotoCreate(BaseModel):
    photo_url: str
    position: int

class PhotoReorder(BaseModel):
    photo_positions: dict[str, int]  # photo_id -> position mapping