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


class Mentor:

    def __init__(self):
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.user_type = "Mentor"
        self.user_id = randint(1000000, 9000000)
        self.subject = choice(subjects)
        self.skill_level = choice(skill_levels)


class MenteeFeedback:

    def __init__(self, mentee_ids, mentor_ids):
        self.ticket_id = randint(1000000, 9000000)
        self.mentee_id = choice(mentee_ids)
        self.mentor_id = choice(mentor_ids)
        self.feedback = choice(feedbacks)


if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    db.reset_collection("Feedbacks")
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    feedbacks = [vars(MenteeFeedback([m['user_id'] for m in mentees],
                                     [m['user_id'] for m in mentors]))
                 for _ in range(200)]
    db.create_many("Feedbacks", feedbacks)