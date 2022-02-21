
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
        self.need = choice(resources)
        self.disability = choice(disability)
        self.work_status = choice(work_status)
        self.poverty_level= choice(poverty_level)
        self.assistance= choice(receiving_assistance)


class Mentor:

    def __init__(self):
        self.first_name = random_first_name()
        self.last_name = choice(last_names)
        self.user_type = "Mentor"
        self.user_id = randint(1000000, 9000000)
        self.subject = choice(subjects)
        self.skill_level = choice(skill_levels)

class Resource:
    def __init__(self):
        self.need = choice(resources)
        self.item_id = randint(1000000, 9000000)




if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

    db.reset_collection("Resources")
    db.create_many("Resources", (vars(Resource()) for _ in range(20)))