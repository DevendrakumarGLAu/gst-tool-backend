from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class RoleCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: Optional[int] = None  # optional, can be filled in controller

class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[int] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_at: Optional[datetime]
    deleted_by: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True
