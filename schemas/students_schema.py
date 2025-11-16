from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from schemas.schema import BaseUserSchema

class StudentRegistrationSchema(BaseUserSchema):
    grade: str
    section: str
    date_of_birth: datetime
    mother_name: str
    mother_contact: str
    father_name: str
    father_contact: str
    roll_number: str
    phone: str
    address: str