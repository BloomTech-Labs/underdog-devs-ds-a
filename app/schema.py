import string
from itertools import chain
from math import ceil, floor
from random import choices, shuffle
from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, constr, Field


class Variants:
    exp_levels = Literal[
        "Beginner", "Intermediate", "Advanced", "Expert",
    ]

    teck_stacks = Literal[
        "Web: HTML, CSS, JavaScript", "Data Science: Python",
        "Android: Java", "iOS: Swift", "Career Development",
        "General Programming",
    ]

class IdGenerator:
    def __call__(self, n_len = 16):  
        n1 = ceil(n_len / 2)
        n2 = floor(n_len / 2)
        prefix = choices(string.ascii_letters, k=n1)
        suffix = map(str, choices(range(0, 9), k=n2))
        uuid_list = list(chain(prefix, suffix))
        shuffle(uuid_list)
        uuid = "".join(uuid_list)
        return uuid

class Mentor(BaseModel):
    profile_id: constr(max_length=16) = Field(default_factory=IdGenerator())
    first_name: constr(max_length=255) = None
    last_name: constr(max_length=255) = None 
    tech_stack: constr(max_length=255) = None
    experience_level: Variants.exp_levels = "General Programming"
    job_help: Optional[bool] = False
    industry_knowledge: Optional[bool] = True
    pair_programming: Optional[bool] = True

class Mentee(BaseModel):
    profile_id: constr(max_length=16) = Field(default_factory=IdGenerator())
    first_name: constr(max_length=255) 
    last_name: constr(max_length=255)
    formerly_incarcerated: Optional[bool] = False
    underrepresented_group: Optional[bool] = False
    low_income: Optional[bool] = False
    list_convictions: List[str] = None
    tech_stack: constr(max_length=255)
    experience_level: Variants.exp_levels  
    job_help: Optional[bool] = False
    pair_programming: Optional[bool] = True
    need: constr(max_length=255) = None
    parole_restriction: Optional[bool] = False
    disability: Optional[bool] = False
    work_status: Optional[bool] = True
    assistance: Optional[bool] = False

class Meeting(BaseModel):
    meeting_id: constr(max_length=16) = Field(default_factory=IdGenerator())
    created_at: datetime = str(datetime.now())
    updated_at: datetime = str(datetime.now())
    meeting_topic: constr(max_length=255) 
    meeting_start_date: datetime   
    meeting_end_date: datetime   
    host_id: constr(max_length=16)  
    attendee_id: constr(max_length=16)
    meeting_notes: constr(max_length=2000) 
    meeting_missed: Literal['Missed', 'Attended'] 

class Feedback(BaseModel):
    ticket_id: constr(max_length=16) = Field(default_factory=IdGenerator())
    mentee_id: constr(max_length=16)
    mentor_id: constr(max_length=16)
    feedback: constr(max_length=2000)

class Resource(BaseModel):
    name: constr(max_length=255)
    item_id: constr(max_length=16) = Field(default_factory=IdGenerator())


if __name__ == '__main__':
    M = Mentor()
    M1 = Mentor()
    M2 = Mentor()

    print(M)
    print(M1)
    print(M2)