from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class CandidateBase(BaseModel):
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education_qualification: str
    graduation_year: int
    years_of_experience: int
    skill_set: List[str]
    
    model_config = ConfigDict(from_attributes=True)

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    contact_number: Optional[str] = None
    contact_address: Optional[str] = None
    education_qualification: Optional[str] = None
    graduation_year: Optional[int] = None
    years_of_experience: Optional[int] = None
    skill_set: Optional[List[str]] = None
    
    model_config = ConfigDict(from_attributes=True)

class CandidateResponse(CandidateBase):
    id: int
    resume_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class CandidateListResponse(BaseModel):
    total: int
    candidates: List[CandidateResponse]

class CandidateFilterParams(BaseModel):
    skill: Optional[str] = None
    experience: Optional[int] = None
    graduation_year: Optional[int] = None
    skip: int = 0
    limit: int = 100