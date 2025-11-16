from pydantic import BaseModel
from typing import Optional

class GSTRequest(BaseModel):
    formData: str 
    gst_number: str
    filing_frequency: Optional[str] = None
    month: Optional[str] = None
    quarter: Optional[str] = None
    year: Optional[str] = None

class GSTResponse(BaseModel):
    message: str
    
    
class GSTDetailsForState(BaseModel):
    gstNumber: str
    filingFrequency: Optional[str] = None
    month: Optional[str] = None
    quarter: Optional[str] = None
    year: Optional[str] = None