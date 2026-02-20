from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional, Any

class FilterPreferenceCreate(BaseModel):
    filter_key: str
    filter_values: List[Any]
    allow_fallback: bool = True

class FilterPreferenceResponse(BaseModel):
    filter_key: str
    filter_values: List[Any]
    allow_fallback: bool