from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, constr


class Variants:
    exp_levels = Literal[
        "Beginner", "Intermediate", "Advanced"
    ]

    teck_stacks = Literal[
        "Web: HTML, CSS, JavaScript", "Data Science: Python",
        "Android: Java", "iOS: Swift", "Career Development",
        "General Programming",
    ]


class Mentor(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    tech_stack: List[str]
    preferred_mentee_exp_level: Variants.exp_levels
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool


class MentorUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    tech_stack: Optional[List[str]]
    preferred_mentee_exp_level: Optional[Variants.exp_levels]
    job_help: Optional[bool]
    industry_knowledge: Optional[bool]
    pair_programming: Optional[bool]


class Mentee(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    formerly_incarcerated: bool
    underrepresented_group: bool
    low_income: bool
    tech_stack: constr(max_length=255)
    experience_level: Variants.exp_levels
    job_help: bool
    pair_programming: bool
    need: Optional[constr(max_length=255)] = None
    parole_restriction: Optional[bool] = False
    disability: Optional[bool] = False
    work_status: Optional[bool] = False
    assistance: Optional[bool] = False


class MenteeUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    formerly_incarcerated: Optional[bool]
    underrepresented_group: Optional[bool]
    low_income: Optional[bool]
    list_convictions: Optional[List[str]]
    tech_stack: Optional[constr(max_length=255)]
    experience_level: Optional[Variants.exp_levels]
    job_help: Optional[bool]
    pair_programming: Optional[bool]
    need: Optional[constr(max_length=255)]
    parole_restriction: Optional[bool]
    disability: Optional[bool]
    work_status: Optional[bool]
    assistance: Optional[bool]


class Meeting(BaseModel):
    meeting_id: constr(max_length=255)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    meeting_topic: Optional[constr(max_length=255)] = None
    meeting_start_date: datetime
    meeting_end_date: datetime
    host_id: constr(max_length=255)
    attendee_id: constr(max_length=255)
    meeting_notes: Optional[constr(max_length=2000)] = None
    meeting_missed: Literal['Missed', 'Attended']


class Feedback(BaseModel):
    ticket_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)
    feedback: Optional[constr(max_length=2000)] = None


class Resource(BaseModel):
    name: constr(max_length=255)
    item_id: constr(max_length=255)
