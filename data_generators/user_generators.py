from random import sample

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


if __name__ == "__main__":
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db._connect("Mentees").create_index("profile_id", unique=True)
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db._connect("Mentors").create_index("profile_id", unique=True)
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    db.reset_collection("Feedbacks")
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    db._connect("Feedbacks").create_index("ticket_id", unique=True)
    feedbacks = [
        vars(
            MenteeFeedback(
                [m["profile_id"] for m in mentees], [m["profile_id"] for m in mentors]
            )
        )
        for _ in range(200)
    ]
    db.create_many("Feedbacks", feedbacks)
