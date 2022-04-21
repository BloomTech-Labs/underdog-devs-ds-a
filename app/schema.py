from typing import Literal, Optional

from pydantic import BaseModel, constr, Field


class Variants:
    experience_level = Literal[
        "Beginner",
        "Intermediate",
        "Advanced",
        "Expert",
    ]
    tech_stack = Literal[
        "Web: HTML, CSS, JavaScript",
        "Data Science: Python",
        "Python",
        "Android: Java",
        "iOS: Swift",
        "Career Development",
        "General Programming",
    ]


class MentorModel(BaseModel):
    profile_id: constr(max_length=64)
    first_name: constr(max_length=255)
    last_name: constr(max_length=255)
    tech_stack: constr(max_length=255)
    experience_level: Variants.experience_level
    job_help: bool
    industry_knowledge: bool
    pair_programming: bool


if __name__ == '__main__':
    m = MentorModel(industry_knowledge=False)
    print(m)
