from random import sample
from typing import List, Dict

from app.data import MongoDB
from data_generators.data_options import *


class Mentor:

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.email = "fake@email.com"
        self.city = "Ashland"
        self.state = "Oregon"
        self.country = "USA"
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.current_comp = choice([
            "Boogle",
            "Amozonian",
            "Poptrist",
            "Macrohard",
            "Pineapple",
        ])
        self.subject = choice(subjects)
        self.experience_level = choice(skill_levels)
        self.job_help = self.subject == "Career Development"
        self.industry_knowledge = percent_true(90)
        self.pair_programming = percent_true(90)
        self.other_info = "Notes"


class Mentee:
    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.email = "fake@email.com"
        self.city = "Ashland"
        self.state = "Oregon"
        self.country = "USA"
        self.formerly_incarcerated = percent_true(80)
        self.underrepresented_group = percent_true(70)
        self.low_income = percent_true(70)
        if self.formerly_incarcerated:
            self.list_convictions = sample(convictions, k=randint(1, 3))
        else:
            self.list_convictions = []
        self.subject = choice(subjects)
        self.experience_level = choice(skill_levels)
        self.job_help = self.subject == "Career Development"
        self.industry_knowledge = percent_true(15)
        if self.job_help:
            self.pair_programming = False
        else:
            self.pair_programming = percent_true(60)
        self.other_info = "Notes"


class MenteeFeedback:
    """Create feedback record from mentee (randomly selected from Mentees Collection) to
    mentor (randomly selected from Mentors Collection), which is stored in Feedbacks Collection.
    1 mentee can give multiple feedbacks to 1 mentor."""

    def __init__(self, mentee_ids, mentor_ids):
        self.mentee_id = choice(mentee_ids)
        self.mentor_id = choice(mentor_ids)
        self.ticket_id = randint(1000000, 9000000)
        self.feedback = choice(feedbacks)


class Meeting:
    '''Create dummy meeting record which is stored in
    meeting collection.'''
    
    def __init__(self, mentee_id, mentor_id ):
        self.meeting_id = randint(1, 10000)
        self.host_id = mentor_id
        self.attendee_id = mentee_id
        '''The following date data may need conversion
        depending how the backend sends their data to us
        They are currently set as a static datetime object'''
        self.created_at = "2018-06-12T09:55:22"
        self.updated_at = "2018-06-12T09:55:22"
        self.meeting_date = "2018-06-12T09:55:22"
        self.meeting_time = "2018-06-12T09:55:22"
        self.meeting_topic = choice(topics)
        self.attended = choice([0,1]) 
        self.meeting_notes = "Meeting notes here!"

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())
        

if __name__ == "__main__":
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db.get_collection("Mentees").create_index("profile_id", unique=True)
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db.get_collection("Mentors").create_index("profile_id", unique=True)
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    db.reset_collection("Feedbacks")
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    db.get_collection("Feedbacks").create_index("ticket_id", unique=True)
    feedbacks = [
        vars(
            MenteeFeedback(
                [m["profile_id"] for m in mentees], [m["profile_id"] for m in mentors]
            )
        )
        for _ in range(200)
    ]
    db.create_many("Feedbacks", feedbacks)


    db.reset_collection("Meetings")
    db.get_collection("Meetings").create_index("meeting_id", unique=True)
    meetings: List[Dict] = [vars(Meeting(
        choice(mentees)["profile_id"],
        choice(mentors)["profile_id"],
    )) for _ in range(50)]
    db.create_many("Meetings", meetings)