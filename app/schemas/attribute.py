from pydantic import BaseModel
from uuid import UUID

class AttributeCreate(BaseModel):
    key: str
    value: str

class AttributeResponse(BaseModel):
    id: UUID
    key: str
    value: str
    user_id: UUID
    
    class Config:
        from_attributes = True
