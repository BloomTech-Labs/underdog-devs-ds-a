from random import sample

import pandas as pd

from data_generators.data_options import *


class Printable:

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


class Mentor(Printable):
    """Mentor Schema"""

    def __init__(self):
        # self.profile_id = generate_uuid(16)
        # self.name = f'{random_first_name()} {choice(last_names)}'
        # self.tech_stack = choice(tech_stack)
        # self.experience_level = choice(skill_levels)
        # self.job_help = self.tech_stack == "Career Development"
        # self.industry_knowledge = percent_true(90)
        # self.pair_programming = percent_true(90)

        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = self.first_name + "." + self.last_name + "@gmail"
        self.located_in_US = percent_true(100)
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.current_company = choice(companies)
        self.current_position = choice(positions)
        self.tech_stack = choice(tech_stack)
        self.preferred_mentee_exp_level = choice(skill_levels)
        self.able_to_commit = percent_true(95)
        self.mentor_contribution = [choice(resource_items), choice(topics),
                                    choice(tech_stack)]
        self.how_heard_about_us = choice(heard_about_us)
        self.anything_else = "anything else may be written here"


class Mentee(Printable):
    """Mentee Schema"""

    def __init__(self):
        # self.profile_id = generate_uuid(16)
        # self.name = f'{random_first_name()} {choice(last_names)}'
        # self.formerly_incarcerated = percent_true(80)
        # self.underrepresented_group = percent_true(70)
        # self.low_income = percent_true(70)
        # if self.formerly_incarcerated:
        #     self.list_convictions = sample(convictions, k=randint(1, 3))
        # else:
        #     self.list_convictions = []
        # self.tech_stack = choice(tech_stack)
        # self.experience_level = choice(skill_levels)
        # self.job_help = self.tech_stack == "Career Development"
        # if self.job_help:
        #     self.pair_programming = False
        # else:
        #     self.pair_programming = percent_true(60)
        # self.need = choice(resource_items)
        # self.parole_restriction = percent_true(50)
        # self.disability = percent_true(15)
        # self.work_status = percent_true(50)
        # self.assistance = percent_true(65)

        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = self.first_name + "." + self.last_name + "@gmail"
        self.located_in_US = percent_true(100)
        self.country = "U.S."
        self.state = choice(states)
        self.city = choice(cities)
        self.formerly_incarcerated = percent_true(80)
        self.underrepresented_group = percent_true(70)
        self.low_income = percent_true(70)
        self.list_convictions = sample(convictions, k=randint(1, 3))
        self.tech_stack = choice(tech_stack)
        self.experience_level = choice(skill_levels)
        self.looking_for = [choice(resource_items), choice(topics),
                            choice(tech_stack)]
        # self.how_heard_about_us = choice(heard_about_us)  -- do we want this question?
        self.anything_else = "anything else may be written here"


class Resource(Printable):
    """ Creates Resource record """

    def __init__(self):
        self.name = choice(resource_items)
        self.item_id = generate_uuid(16)


class MenteeFeedback(Printable):
    """Create feedback record from mentee (randomly selected from Mentees Collection) to
    mentor (randomly selected from Mentors Collection), which is stored in Feedbacks Collection.
    1 mentee can give multiple feedbacks to 1 mentor."""
    feedback = pd.read_csv("review.csv", index_col="Id")

    def __init__(self, mentee_id, mentor_id):
        self.ticket_id = generate_uuid(16)
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.feedback = choice(self.feedback["Review"])


class Meeting(Printable):
    """Create dummy meeting record which is stored in
    meeting collection."""

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
