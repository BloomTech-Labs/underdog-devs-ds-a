from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, constr, Extra


# TODO add pydantic to requirements.txt


class Mentor(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: constr(max_length=255)
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    current_company: constr(max_length=255)
    current_position: constr(max_length=255)
    tech_stack: constr(max_length=255)
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool
    able_to_commit: bool
    how_heard_about_us: constr(max_length=255)
    anything_else: constr(max_length=2500)


class MentorUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[constr(max_length=255)]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    current_company: Optional[constr(max_length=255)]
    current_position: Optional[constr(max_length=255)]
    tech_stack: Optional[constr(max_length=255)]
    job_help: Optional[bool]
    industry_knowledge: Optional[bool]
    pair_programming: Optional[bool]
    able_to_commit: Optional[bool]
    how_heard_about_us: Optional[constr(max_length=255)]
    anything_else: Optional[constr(max_length=2500)]

    class Config:
        extra = Extra.forbid


class Mentee(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: constr(max_length=255)
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    formerly_incarcerated: bool
    underrepresented_group: bool
    low_income: bool
    list_convictions: constr(max_length=255)
    tech_stack: constr(max_length=255)
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool
    how_heard_about_us: constr(max_length=255)
    anything_else: Optional[constr(max_length=2500)]


class MenteeUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[constr(max_length=255)]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    formerly_incarcerated: Optional[bool]
    underrepresented_group: Optional[bool]
    low_income: Optional[bool]
    list_convictions: Optional[constr(max_length=255)]
    tech_stack: Optional[constr(max_length=255)]
    job_help: Optional[bool]
    industry_knowledge: Optional[bool]
    pair_programming: Optional[bool]
    how_heard_about_us: Optional[constr(max_length=255)]
    anything_else: Optional[constr(max_length=2500)]

    class Config:
        extra = Extra.forbid


class Meeting(BaseModel):
    meeting_id: constr(max_length=255)
    created_at: datetime
    updated_at: datetime
    meeting_topic: constr(max_length=255)
    meeting_start_date: datetime
    meeting_end_date: datetime
    host_id: constr(max_length=255)
    attendee_id: constr(max_length=255)
    meeting_notes: Optional[constr(max_length=2000)]
    meeting_missed: Optional[Literal['Missed', 'Attended']]


class MeetingUpdate(BaseModel):
    meeting_id: Optional[constr(max_length=255)]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    meeting_topic: Optional[constr(max_length=255)]
    meeting_start_date: Optional[datetime]
    meeting_end_date: Optional[datetime]
    host_id: Optional[constr(max_length=255)]
    attendee_id: Optional[constr(max_length=255)]
    meeting_notes: Optional[constr(max_length=2000)]
    meeting_missed: Optional[Literal['Missed', 'Attended']]


class Feedback(BaseModel):
    ticket_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)
    feedback: Optional[constr(max_length=2000)]


class Resource(BaseModel):
    name: constr(max_length=255)
    item_id: constr(max_length=255)
