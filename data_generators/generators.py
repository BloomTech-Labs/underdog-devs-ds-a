import os
from typing import List, Any
from random import sample, triangular

import pandas as pd

from data_generators.data_options import *
from app.sentiment import sentiment_rank


class Printable:
    """Parent Class"""

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


class LinearChoice:

    def __init__(self, values: List[Any]):
        self.values = values
        self.size = len(values)

    def front(self) -> Any:
        return self.values[int(triangular(0, self.size, 0))]

    def middle(self) -> Any:
        return self.values[int(triangular(0, self.size, self.size / 2))]

    def back(self) -> Any:
        return self.values[int(triangular(0, self.size, self.size))]


class RandomMentor(Printable):
    """Generates Mentor record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name(percent_male=75)
        self.last_name = choice(last_names)
        self.email = f"{self.first_name}.{self.last_name}@gmail.com"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.current_company = choice(companies)
        self.current_position = choice(positions)
        self.tech_stack = list({
            LinearChoice(tech_stack).back()
            for _ in range(randint(1, 5))
        })
        self.commitment = percent_true(95)
        self.job_help = percent_true(33)
        self.industry_knowledge = percent_true(33)
        self.pair_programming = percent_true(33)
        self.referred_by = choice(heard_about_us)
        self.other_info = "anything else may be written here"
        self.validate_status = choice(["approved", "pending"])
        self.is_active = percent_true(80)
        self.accepting_new_mentees = percent_true(80)


class RandomMentee(Printable):
    """Generates Mentee record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name(percent_male=75)
        self.last_name = choice(last_names)
        self.email = f"{self.first_name}.{self.last_name}@gmail.com"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.formerly_incarcerated = percent_true(80)
        self.underrepresented_group = percent_true(70)
        self.low_income = percent_true(70)
        self.convictions = ", ".join(sample(convictions, k=randint(1, 3)))
        self.tech_stack = LinearChoice(tech_stack).front()
        self.job_help = percent_true(33)
        self.pair_programming = percent_true(33)
        self.referred_by = choice(heard_about_us)
        self.other_info = "anything else may be written here"
        self.validate_status = choice(["approved", "pending"])
        self.is_active = percent_true(80)
        self.in_project_underdog = percent_true(15)


class RandomMenteeFeedback(Printable):
    """Generates Feedback record from mentee"""
    file_path = os.path.join("data_generators", "review.csv")
    feedback = pd.read_csv(file_path, index_col="Id")

    def __init__(self, mentee_id, mentor_id):
        self.ticket_id = generate_uuid(16)
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.text = choice(self.feedback["Review"])
        self.sentiment = sentiment_rank(self.text)


class RandomMeeting(Printable):
    """Generates Meeting record"""

    def __init__(self, mentee_id, mentor_id):
        self.meeting_id = generate_uuid(16)
        self.meeting_topic = choice(topics)
        self.meeting_start_time = random_datetime(
            datetime(2022, 1, 1),
            datetime(2022, 12, 31),
        )
        self.meeting_end_time = self.meeting_start_time + timedelta(hours=1)
        self.mentor_id = mentor_id
        self.mentee_id = mentee_id
        self.admin_meeting_notes = "Meeting notes here!"
        self.meeting_missed_by_mentee = choice(['Missed', 'Attended'])
        self.mentor_meeting_notes = "Mentor meeting notes"
        self.mentee_meeting_notes = "Mentee meeting notes"
