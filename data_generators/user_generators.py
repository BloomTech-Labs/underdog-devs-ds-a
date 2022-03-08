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

    def __init__(self, mentee_id, mentor_id):
        self.ticket_id = generate_uuid(16)
        self.mentee_id = mentee_id
        self.mentor_id = mentor_id
        self.feedback = choice(feedbacks)

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())


if __name__ == "__main__":
    db = MongoDB("UnderdogDevs")

    # db.reset_collection("Mentees")
    # db.get_collection("Mentees").create_index("profile_id", unique=True)
    # db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    # db.reset_collection("Mentors")
    # db.get_collection("Mentors").create_index("profile_id", unique=True)
    # db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    # mentees = db.read("Mentees")
    # mentors = db.read("Mentors")

    # db.delete("Feedback", {})
    # db.get_collection("Feedback").create_index("ticket_id", unique=True)

    # feedback = [vars(MenteeFeedback(
    #     choice(mentees)["profile_id"],
    #     choice(mentors)["profile_id"],
    # )) for _ in range(100)]
    # db.create_many("Feedback", feedback)
