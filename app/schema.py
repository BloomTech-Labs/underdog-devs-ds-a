from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, constr, Field
from uuid import uuid4, UUID

class Variants:
    exp_levels = Literal[
        "Beginner", "Intermediate", "Advanced", "Expert",
    ]

    teck_stacks = Literal[
        "Web: HTML, CSS, JavaScript", "Data Science: Python",
        "Android: Java", "iOS: Swift", "Career Development",
        "General Programming",
    ]

class Mentor(BaseModel):
    profile_id: constr(max_length=16)         
    first_name: constr(max_length=255) = "Maria"
    last_name: constr(max_length=255) = "Perez"      
    tech_stack: constr(max_length=255) = "App Dev"
    experience_level: Variants.exp_levels = "Beginner"
    job_help: Optional[bool] = False
    industry_knowledge: bool    = False
    pair_programming: bool   = False

class Mentee(BaseModel):
    profile_id: constr(max_length=16) #UUID = Field(default_factory=uuid4)
    first_name: constr(max_length=255) 
    last_name: constr(max_length=255) = None
    formerly_incarcerated: Optional[bool] = False
    underrepresented_group: Optional[bool] = False
    low_income: Optional[bool] = False
    list_convictions: List[str] = None
    tech_stack: constr(max_length=255)
    experience_level: Variants.exp_levels  
    job_help: Optional[bool] = False
    pair_programming: bool
    need: constr(max_length=255) = None
    parole_restriction: bool
    disability: bool
    work_status: bool
    assistance: bool

class Meeting(BaseModel):
    meeting_id: str
    created_at: datetime
    updated_at: datetime
    meeting_topic: str
    meeting_start_date: datetime
    meeting_end_date: datetime
    host_id: str
    attendee_id: str
    meeting_notes = constr(max_length=2000)
    meeting_missed = Literal['Missed', 'Attended']

class Feedback(BaseModel):
    ticket_id: str
    mentee_id: str
    mentor_id: str
    feedback: constr(max_length=2000)

class Resource(BaseModel):
    name: constr(max_length=255)
    item_id: str

if __name__ == '__main__':
    M = Mentor()

    print(M)