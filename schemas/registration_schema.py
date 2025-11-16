# schemas/registration_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role_id: int
    created_by: Optional[int] = None

class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UpdateRegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role_id: Optional[int] = None
    updated_by: Optional[str] = None
    
class UnifiedRegistrationSchema(BaseModel):
    # Common Fields
    email: EmailStr
    password: str
    full_name: str
    role_id: int  # 1 = student, 2 = teacher
    phone: str
    address: str

    # Student Fields (optional)
    grade: Optional[str]
    section: Optional[str]
    date_of_birth: Optional[datetime]
    mother_name: Optional[str]
    mother_contact: Optional[str]
    father_name: Optional[str]
    father_contact: Optional[str]
    roll_number: Optional[str]

    # Teacher Fields (optional)
    department: Optional[str]
    subjects_taught: Optional[str]
    hire_date: Optional[datetime]
    employee_id: Optional[str]