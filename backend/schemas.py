from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
