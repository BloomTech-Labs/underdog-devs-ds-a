import os
from uuid import uuid4
from datetime import datetime, timedelta
from typing import List, Any
from random import sample, triangular, random, choice, randint

import pandas as pd

from app.sentiment import sentiment_rank
from data_generators.data_options import male_first_names, female_first_names, last_names, states, cities, companies, \
    positions, tech_stack, heard_about_us, convictions, topics


def percent_true(percent: int) -> bool:
    return 100 * random() < percent


def random_first_name(percent_male: int):
    if percent_true(percent_male):
        return choice(male_first_names)
    else:
        return choice(female_first_names)


def random_datetime(start: datetime, end: datetime) -> datetime:
    """ Returns a random datetime between start and end """
    delta = end - start
    random_second = randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_second)


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
        self.profile_id = str(uuid4())
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
        self.profile_id = str(uuid4())
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
        self.ticket_id = str(uuid4())
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.text = choice(self.feedback["Review"])
        self.sentiment = sentiment_rank(self.text)


class RandomMeeting(Printable):
    """Generates Meeting record"""

    def __init__(self, mentee_id, mentor_id):
        self.meeting_id = str(uuid4())
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
