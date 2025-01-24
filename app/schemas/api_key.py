from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ApiKeyCreate(BaseModel):
    key_name: str

class ApiKeyResponse(BaseModel):
    id: UUID
    key: str | None = None
    prefix: str
    key_name: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True