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


class Feedback:

    def __init__(self, mentees_ids, mentors_ids):
        self.mentee_id = choice(mentees_ids)
        self.mentor_id = choice(mentors_ids)
        self.ticket_id = randint(1000000, 9000000)
        self.feedback = choice(feedbacks)

if __name__ == '__main__':

    # codes from github
    db = MongoDB("UnderdogDevs")
    db._connect("Mentees").drop()
    db.reset_collection("Mentees")
    db.create_many("Mentees", [vars(Mentee()) for _ in range(100)])
    db._connect("Mentors").drop()
    db.reset_collection("Mentors")
    db.create_many("Mentors", [vars(Mentor()) for _ in range(20)])
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    db._connect("Feedbacks").drop()
    db.reset_collection("Feedbacks")
    feedbacks = [vars(Feedback([m['user_id'] for m in mentees],
                             [m['user_id'] for m in mentors]))
               for i in range(200)]
    db.create_many("Feedbacks", feedbacks)

