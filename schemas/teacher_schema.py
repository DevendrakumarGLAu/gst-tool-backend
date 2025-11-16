from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from schemas.schema import BaseUserSchema

class TeacherRegistrationSchema(BaseUserSchema):
    department: str
    subjects_taught: str
    hire_date: datetime
    employee_id: str
    phone: str
    address: str