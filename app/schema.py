from typing import Literal, Optional, List
from datetime import datetime
from pydantic import BaseModel, constr, Extra, EmailStr, conint


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
    referred_by: constr(max_length=255)
    other_info: Optional[constr(max_length=2500)]
    validate_status: constr(max_length=255)

    class Config:
        extra = Extra.forbid


class MentorUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
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
    validate_status: Optional[constr(max_length=255)]

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
    list_convictions: List[constr(max_length=255)]
    tech_stack: constr(max_length=255)
    job_help: bool
    pair_programming: bool
    heard_about: constr(max_length=255)
    other_info: Optional[constr(max_length=2500)]
    validate_status: constr(max_length=255)

    class Config:
        extra = Extra.forbid


class MenteeUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[EmailStr]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    formerly_incarcerated: Optional[bool]
    underrepresented_group: Optional[bool]
    low_income: Optional[bool]
    list_convictions: Optional[List[constr(max_length=255)]]
    tech_stack: Optional[constr(max_length=255)]
    job_help: Optional[bool]
    pair_programming: Optional[bool]
    heard_about: Optional[constr(max_length=255)]
    other_info: Optional[constr(max_length=2500)]
    validate_status: Optional[constr(max_length=255)]

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


class TicketsTable(BaseModel):
    ticket_id: constr(max_length=255)
    ticket_type: Optional[Literal['Action', 'Application', 'Resource', 'Role']]
    ticket_status: Optional[Literal['Pending', 'Approved', 'Rejected']]
    ticket_subject: constr(max_length=255)
    urgent: Optional[Literal['Low', 'Normal', 'High']]
    notes: constr(max_length=255)
    requested_for: constr(max_length=255)
    submitted_by: constr(max_length=255)
    approved_by: constr(max_length=255)


class Assignment(BaseModel):
    mentor_id: constr(max_length=255)
    mentee_id: constr(max_length=255)
    assignment_id: constr(max_length=255)


class Resources(BaseModel):
    resource_id: constr(max_length=255)
    updated_at: constr(max_length=255)
    resource_name: constr(max_length=255)
    category: constr(max_length=255)
    condition: constr(max_length=255)
    assigned: constr(max_length=255)
    current_assignee: constr(max_length=255)
    previous_assignee: constr(max_length=255)
    monetary_value: constr(max_length=255)
    deductible_donation: constr(max_length=255)


class Reviews(BaseModel):
    review_id: constr(max_length=255)
    review: constr(max_length=255)
    rating: conint(ge=1, le=5)
    mentee_id: constr(max_length=255)
    mentor_id: constr(max_length=255)
