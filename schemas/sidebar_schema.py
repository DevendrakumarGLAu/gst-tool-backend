# schemas/sidebar_schema.py
from pydantic import BaseModel
from typing import Optional, List

class SidebarCreateRequest(BaseModel):
    title: str
    path: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    role_ids: Optional[List[int]] = []

class SidebarUpdateRequest(BaseModel):
    title: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    role_ids: Optional[List[int]] = []

class SidebarResponse(BaseModel):
    id: int
    title: str
    path: str
    icon: Optional[str]
    parent_id: Optional[int]
    role_ids: List[int]

    class Config:
        from_attributes = True
