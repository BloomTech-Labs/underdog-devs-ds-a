from typing import Literal, Optional, List
from datetime import datetime
from pydantic import BaseModel, constr, Extra, EmailStr


class Mentor(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    current_company: constr(max_length=255)
    current_position: constr(max_length=255)
    tech_stack: List[constr(max_length=255)]
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool
    commitment: bool
    referred_by: Optional[constr(max_length=255)]
    other_info: Optional[constr(max_length=2500)]
    validate_status: Literal['approved', 'rejected', 'pending']
    is_active: bool
    accepting_new_mentees: bool

    class Config:
        extra = Extra.forbid


class MentorUpdate(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[EmailStr]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    current_company: Optional[constr(max_length=255)]
    current_position: Optional[constr(max_length=255)]
    tech_stack: Optional[List[constr(max_length=255)]]
    job_help: Optional[bool]
    industry_knowledge: Optional[bool]
    pair_programming: Optional[bool]
    commitment: Optional[bool]
    referred_by: Optional[constr(max_length=255)]
    other_info: Optional[constr(max_length=2500)]
    validate_status: Optional[Literal['approved', 'rejected', 'pending']]
    is_active: Optional[bool]
    accepting_new_mentees: Optional[bool]

    class Config:
        extra = Extra.forbid


class Mentee(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: EmailStr
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    formerly_incarcerated: bool
    underrepresented_group: bool
    low_income: bool
    convictions: Optional[constr(max_length=2500)]
    tech_stack: constr(max_length=255)
    job_help: bool
    pair_programming: bool
    referred_by: constr(max_length=255)
    other_info: Optional[constr(max_length=2500)]
    validate_status: Literal['approved', 'rejected', 'pending']
    is_active: bool
    in_project_underdog: bool

    class Config:
        extra = Extra.forbid


class MenteeUpdate(BaseModel):
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[EmailStr]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    formerly_incarcerated: Optional[bool]
    underrepresented_group: Optional[bool]
    low_income: Optional[bool]
    convictions: Optional[constr(max_length=2500)]
    tech_stack: Optional[constr(max_length=255)]
    job_help: Optional[bool]
    pair_programming: Optional[bool]
    referred_by: Optional[constr(max_length=255)] 
    other_info: Optional[constr(max_length=2500)]
    validate_status: Optional[Literal['approved', 'rejected', 'pending']]
    is_active: Optional[bool]
    in_project_underdog: Optional[bool]

    class Config:
        extra = Extra.forbid


class Meeting(BaseModel):
    meeting_id: constr(max_length=255)
    meeting_topic: constr(max_length=255)
    meeting_start_time: datetime
    meeting_end_time: datetime
    mentor_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    admin_meeting_notes: Optional[constr(max_length=2000)]
    meeting_missed_by_mentee: Optional[Literal['Missed', 'Attended']]
    mentor_meeting_notes: Optional[constr(max_length=2000)]
    mentee_meeting_notes: Optional[constr(max_length=2000)]

    class Config:
        extra = Extra.forbid


class MeetingUpdate(BaseModel):
    meeting_topic: Optional[constr(max_length=255)]
    meeting_start_time: Optional[datetime]
    meeting_end_time: Optional[datetime]
    mentor_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    admin_meeting_notes: Optional[constr(max_length=2000)]
    meeting_missed_by_mentee: Optional[Literal['Missed', 'Attended']]
    mentor_meeting_notes: Optional[constr(max_length=2000)]
    mentee_meeting_notes: Optional[constr(max_length=2000)]

    class Config:
        extra = Extra.forbid


class Feedback(BaseModel):
    text: constr(max_length=800)
    ticket_id: constr(max_length=16)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)

    class Config:
        extra = Extra.forbid


class FeedbackUpdate(BaseModel):
    text: Optional[constr(max_length=255)]
    mentee_id: Optional[constr(max_length=255)]
    mentor_id: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class FeedbackOptions(BaseModel):
    ticket_id: Optional[constr(max_length=16)]
    mentee_id: Optional[constr(max_length=255)]
    mentor_id: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid
