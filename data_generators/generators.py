import os
from random import sample, randint

import pandas as pd
from datetime import datetime

from data_generators.data_options import *


class Printable:
    """Parent Class"""

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


class RandomMentor(Printable):
    """Generates Mentor record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = f"{self.first_name}.{self.last_name}@gmail.com"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.current_company = choice(companies)
        self.current_position = choice(positions)
        self.tech_stack = sample(tech_stack, k=randint(1, 3))
        self.commitment = percent_true(95)
        self.job_help = percent_true(33)
        self.industry_knowledge = percent_true(33)
        self.pair_programming = percent_true(33)
        self.referred_by = choice(heard_about_us)
        self.other_info = "anything else may be written here"
        self.validate_status = choice(["approved", "pending"])
        self.is_active = percent_true(80)
        self.accepting_new_mentees = percent_true(33)


class RandomMentee(Printable):
    """Generates Mentee record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = f"{self.first_name}.{self.last_name}@gmail.com"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.formerly_incarcerated = percent_true(80)
        self.underrepresented_group = percent_true(70)
        self.low_income = percent_true(70)
        self.list_convictions = sample(convictions, k=randint(1, 3))
        self.tech_stack = choice(tech_stack)
        self.job_help = percent_true(33)
        self.pair_programming = percent_true(33)
        self.heard_about = choice(heard_about_us)
        self.other_info = "anything else may be written here"
        self.validate_status = choice(["approved", "pending"])
        self.is_active = percent_true(80)
        self.in_project_underdog = percent_true(15)


class RandomResource(Printable):
    """Generates Resource record"""

    def __init__(self):
        self.name = choice(resource_items)
        self.item_id = generate_uuid(16)


class RandomMenteeFeedback(Printable):
    """Generates Feedback record from mentee"""
    file_path = os.path.join("data_generators", "review.csv")
    feedback = pd.read_csv(file_path, index_col="Id")

    def __init__(self, mentee_id, mentor_id):
        self.ticket_id = generate_uuid(16)
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.feedback = choice(self.feedback["Review"])
        self.datetime = datetime.now()


class RandomMeeting(Printable):
    """Generates Meeting record"""

    def __init__(self, mentee_id, mentor_id):
        self.meeting_id = generate_uuid(16)
        self.meeting_topic = choice(topics)
        self.meeting_start_date = "2018-06-12T09:55:22"
        self.meeting_end_date = "2018-06-12T09:55:22"
        self.host_id = mentor_id
        self.attendee_id = mentee_id
        self.meeting_notes = "Meeting notes here!"
        self.meeting_missed = choice(['Missed', 'Attended'])
