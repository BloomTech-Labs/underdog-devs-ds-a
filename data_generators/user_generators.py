
from importlib import resources
from app.data import MongoDB
from data_generators.data_options import *


class Mentee:

    def __init__(self):
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.user_type = "Mentee"
        self.user_id = randint(1000000, 9000000)
        self.subject = choice(subjects)
        self.skill_level = choice(skill_levels)
        self.need = choice(resource_items)
        self.disability = choice(disability)
        self.work_status = choice(work_status)
        self.assistance = choice(receiving_assistance)


class Mentor:

    def __init__(self):
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.user_type = "Mentor"
        self.user_id = randint(1000000, 9000000)
        self.subject = choice(subjects)
        self.skill_level = choice(skill_levels)


class Resource:
    """ Creates Resource record """

    def __init__(self):
        self.need = choice(resource_items)
        self.item_id = randint(1000000, 9000000)


class MenteeFeedback:
    """Create feedback record from mentee (randomly selected from Mentees Collection) to
    mentor (randomly selected from Mentors Collection), which is stored in Feedbacks Collection.
    1 mentee can give multiple feedbacks to 1 mentor."""

    def __init__(self, mentee_ids, mentor_ids):
        self.mentee_id = choice(mentee_ids)
        self.mentor_id = choice(mentor_ids)
        self.ticket_id = randint(1000000, 9000000)
        self.feedback = choice(feedbacks)


if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db._connect("Mentees").create_index("user_id", unique=True)
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db._connect("Mentors").create_index("user_id", unique=True)
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    db.reset_collection("Resources")
    db.create_many("Resources", (vars(Resource()) for _ in range(20)))
    db.reset_collection("Feedbacks")
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    db._connect("Feedbacks").create_index("ticket_id", unique=True)
    feedbacks = [vars(MenteeFeedback([m['user_id'] for m in mentees],
                                     [m['user_id'] for m in mentors]))
                 for _ in range(200)]
    db.create_many("Feedbacks", feedbacks)
