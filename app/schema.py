from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, constr


EXP_LEVELS = Literal[
    "Beginner", "Intermediate", "Advanced", "Expert",
]

TECH_STACKS = Literal[
    "Web: HTML, CSS, JavaScript", "Data Science: Python",
    "Android: Java", "iOS: Swift", "Career Development",
    "General Programming",
]

class Mentor(BaseModel):
    profile_id: str         
    name: constr(max_length=255)             
    tech_stack: TECH_STACKS
    experience_level: EXP_LEVELS   
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool

class Mentee(BaseModel):
    profile_id: str
    name: constr(max_length=255) 
    formerly_incarcerated: bool = False
    underrepresented_group: bool = False
    low_income: bool = False
    list_convictions: List[str] = None
    tech_stack: TECH_STACKS 
    experience_level: EXP_LEVELS 
    job_help: bool = False
    pair_programming: bool = False
    need: constr(max_length=255) = None
    parole_restriction: bool = False
    disability: bool = False
    work_status: bool = False
    assistance: bool = False

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