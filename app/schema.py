from typing import Literal, Optional, List
from datetime import datetime
from pydantic import BaseModel, constr, Extra, EmailStr, conint


class Mentor(BaseModel):
    profile_id: constr(max_length=255)
    created_at: datetime
    updated_at: datetime
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
    profile_id: constr(max_length=255)
    updated_at: datetime
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
    created_at: datetime
    updated_at: datetime
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
    heard_about: constr(max_length=255)
    other_info: Optional[constr(max_length=2500)]
    validate_status: Literal['approved', 'rejected', 'pending']
    is_active: bool
    in_project_underdog: bool

    class Config:
        extra = Extra.forbid


class MenteeUpdate(BaseModel):
    profile_id: constr(max_length=255)
    updated_at: datetime
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
    heard_about: Optional[constr(max_length=255)]
    other_info: Optional[constr(max_length=2500)]
    validate_status: Optional[Literal['approved', 'rejected', 'pending']]
    is_active: Optional[bool]
    in_project_underdog: Optional[bool]

    class Config:
        extra = Extra.forbid


class Meeting(BaseModel):
    meeting_id: constr(max_length=255)
    created_at: datetime
    updated_at: datetime
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
    meeting_id: Optional[constr(max_length=255)]
    created_at: Optional[datetime]
    updated_at: datetime
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
    ticket_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)
    feedback: Optional[constr(max_length=2000)]



class Role(BaseModel):
    """schema mirrored from BE's postgres db"""
    role_id: constr(max_length=255)
    role_name: Literal['superAdmin', 'admin', 'mentor', 'mentee', 'pending']


class Comments(BaseModel):
    """schema mirrored from BE's postgres db"""
    comment_id: constr(max_length=255)
    comment_text: Optional[constr(max_length=2000)]
    created_at: datetime
    note_id: constr(max_length=255)
    updated_at: datetime


class Notes(BaseModel):
    """schema mirrored from BE's postgres db"""
    note_id: constr(max_length=255)
    created_by: constr(max_length=255)
    status: Literal['in progress', 'resolved', 'no action needed', 'escalated']
    content_type: constr(max_length=255)
    content: constr(max_length=255)
    level: constr(max_length=255)
    visible_to_admin: Optional[bool]
    visible_to_mentor: Optional[bool]
    visible_to_mentee: Optional[bool]
    created_at: datetime
    updated_at: datetime
    mentor_id: constr(max_length=255)
    mentee_id: constr(max_length=255)


class MenteeProgression(BaseModel):
    """schema mirrored from BE's postgres db"""
    progress_id: constr(max_length=255)
    progress: Literal['learning', 'in_program', 'interview_prep', 'applying/interviewing', 'hired']


class TicketsTable(BaseModel):
    """schema mirrored from BE's postgres db"""
    ticket_id: constr(max_length=255)
    ticket_type: Literal['Action', 'Application', 'Resource', 'Role']
    ticket_status: Literal['Pending', 'Approved', 'Rejected']
    ticket_subject: constr(max_length=255)
    urgent: Optional[Literal['Low', 'Normal', 'High']]
    notes: constr(max_length=255)
    requested_for: constr(max_length=255)
    submitted_by: constr(max_length=255)
    approved_by: constr(max_length=255)


class Assignment(BaseModel):
    """schema mirrored from BE's postgres db"""
    mentor_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    assignment_id: constr(max_length=255)


class Resources(BaseModel):
    """schema mirrored from BE's postgres db
    not part of MVP, stretch goal"""
    resource_id: constr(max_length=255)
    updated_at: constr(max_length=255)
    resource_name: constr(max_length=255)
    category: constr(max_length=255)
    condition: constr(max_length=255)
    assigned: constr(max_length=255)
    current_assignee: constr(max_length=255)
    previous_assignee: constr(max_length=255)
    monetary_value: float
    deductible_donation: bool


class Reviews(BaseModel):
    """schema mirrored from BE's postgres db"""
    review_id: constr(max_length=255)
    review: constr(max_length=255)
    rating: conint(ge=1, le=5)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)
