from random import sample

import pandas as pd

from data_generators.data_options import *


class Printable:
    """Parent Class"""

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


class Mentor(Printable):
    """Generates Mentor record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = self.first_name + "." + self.last_name + "@gmail"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.current_company = choice(companies)
        self.current_position = choice(positions)
        self.tech_stack = choice(tech_stack)
        self.able_to_commit = percent_true(95)
        self.job_help = percent_true(33)
        self.industry_knowledge = percent_true(33)
        self.pair_programming = percent_true(33)
        self.how_heard_about_us = choice(heard_about_us)
        self.anything_else = "anything else may be written here"


class Mentee(Printable):
    """Generates Mentee record"""

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = self.first_name + "." + self.last_name + "@gmail"
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.formerly_incarcerated = percent_true(80)
        self.underrepresented_group = percent_true(70)
        self.low_income = percent_true(70)
        self.list_convictions = sample(convictions, k=randint(1, 3))[0]
        self.tech_stack = choice(tech_stack)
        self.job_help = percent_true(33)
        self.industry_knowledge = percent_true(33)
        self.pair_programming = percent_true(33)
        self.anything_else = "anything else may be written here"


class Resource(Printable):
    """Generates Resource record"""

    def __init__(self):
        self.name = choice(resource_items)
        self.item_id = generate_uuid(16)


class MenteeFeedback(Printable):
    """Generates Feedback record from mentee"""

    feedback = pd.read_csv("review.csv", index_col="Id")

    def __init__(self, mentee_id, mentor_id):
        self.ticket_id = generate_uuid(16)
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.feedback = choice(self.feedback["Review"])


class Meeting(Printable):
    """Generates Meeting record"""

    def __init__(self, mentee_id, mentor_id):
        self.meeting_id = generate_uuid(16)
        self.created_at = "2018-06-12T09:55:22"
        self.updated_at = "2018-06-12T09:55:22"
        self.meeting_topic = choice(topics)
        self.meeting_start_date = "2018-06-12T09:55:22"
        self.meeting_end_date = "2018-06-12T09:55:22"
        self.host_id = mentor_id
        self.attendee_id = mentee_id
        self.meeting_notes = "Meeting notes here!"
        self.meeting_missed = choice(['Missed', 'Attended'])
