from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class FreelancerProfile(BaseModel):
    name: str
    skills: List[str]
    experience: str
    past_projects: List[str]
    rates: Optional[str] = None
    bio: Optional[str] = None

class JobPosting(BaseModel):
    title: str
    description: str
    requirements: List[str]
    budget: Optional[str] = None
    timeline: Optional[str] = None
    key_priorities: Optional[List[str]] = None

class ProposalRequest(BaseModel):
    job_posting: str
    tone: Optional[str] = "professional"

class ProposalResponse(BaseModel):
    proposal: str
    confidence_score: float
    matched_skills: List[str]
    generated_at: datetime

class StoredProposal(BaseModel):
    id: str
    job_posting: str
    proposal: str
    confidence_score: float
    generated_at: datetime