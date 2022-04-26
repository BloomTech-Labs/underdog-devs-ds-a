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
    email: constr(max_length=255)
    located_in_US: bool
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    current_company: constr(max_length=255)
    current_position: constr(max_length=255)
    tech_stack: List[str]
    preferred_mentee_exp_level: Variants.exp_levels
    able_to_commit: bool
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool
    how_heard_about_us: constr(max_length=255)


class MentorUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[constr(max_length=255)]
    located_in_US: Optional[bool]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    current_company: Optional[constr(max_length=255)]
    current_position: Optional[constr(max_length=255)]
    tech_stack: Optional[List[str]]
    preferred_mentee_exp_level: Optional[Variants.exp_levels]
    able_to_commit: Optional[bool]
    job_help: Optional[bool]
    industry_knowledge: Optional[bool]
    pair_programming: Optional[bool]
    how_heard_about_us: Optional[constr(max_length=255)]


class Mentee(BaseModel):
    profile_id: constr(max_length=255)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    email: constr(max_length=255)
    located_in_US: bool
    country: constr(max_length=255)
    state: constr(max_length=255)
    city: constr(max_length=255)
    formerly_incarcerated: bool
    underrepresented_group: bool
    low_income: bool
    list_convictions: Optional[List[str]]
    tech_stack: constr(max_length=255)
    experience_level: Variants.exp_levels
    looking_for_job_help: bool
    looking_for_industry_knowledge: bool
    looking_to_pair_programming: bool


class MenteeUpdate(BaseModel):
    profile_id: Optional[constr(max_length=255)]
    first_name: Optional[constr(max_length=255)]
    last_name: Optional[constr(max_length=255)]
    email: Optional[constr(max_length=255)]
    located_in_US: Optional[bool]
    country: Optional[constr(max_length=255)]
    state: Optional[constr(max_length=255)]
    city: Optional[constr(max_length=255)]
    formerly_incarcerated: Optional[bool]
    underrepresented_group: Optional[bool]
    low_income: Optional[bool]
    list_convictions: Optional[List[str]]
    tech_stack: Optional[constr(max_length=255)]
    experience_level: Optional[Variants.exp_levels]
    looking_for_job_help: Optional[bool]
    looking_for_industry_knowledge: Optional[bool]
    looking_to_pair_programming: Optional[bool]


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
