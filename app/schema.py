from typing import List, Optional
from pydantic import BaseModel


class Mentor(BaseModel):
    profile_id: str         
    email:	Optional[str] = None
    location: Optional[str] = None
    name: str 
    current_comp: Optional[str] = None              
    tech_stack: str #List[str]   
    experience_level: str   
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool

class Mentee(BaseModel):
    profile_id: str	 
    email: str	 
    location: str	 
    name: str	 
    lives_in_us: bool	 
    formerly_incarcerated: bool
    list_convictions: str	 
    tech_stack: str	 
    experience_level: str	 
    your_hope: str	 
    other_info: str	 