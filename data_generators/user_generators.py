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


if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))
