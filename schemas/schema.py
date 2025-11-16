from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: str
    access_token: str
    token_type: str
    role: str
    
class BaseUserSchema(BaseModel):
    created_by: Optional[int]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class UserUpdateBaseSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role_id: Optional[int] = None
    updated_by: Optional[str] = None  # ID or username of the user performing the update
    
    class Config:
        from_attributes = True  # Ensures compatibility with Django models

class StudentUpdateSchema(UserUpdateBaseSchema):
    phone: Optional[str] = None
    grade: Optional[str] = None
    section: Optional[str] = None
    date_of_birth: Optional[str] = None

class TeacherUpdateSchema(UserUpdateBaseSchema):
    subject: Optional[str] = None
    department: Optional[str] = None