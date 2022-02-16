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

    def __init__(self, mentees_ids, mentors_ids):
        self.mentee_id = choice(mentees_ids)
        self.mentor_id = choice(mentors_ids)
        self.ticket_id = int(str(self.mentee_id) + str(self.mentor_id))
        self.feedback = choice(feedbacks)

def create_many(collection, number_records):

    if collection == 'Mentees':
        try:
            db._connect(collection).drop()
            db._connect(collection).create_index("user_id", unique=True)
            db.create_many(collection, (vars(Mentee()) for _ in range(number_records)))
        except:
            create_many(collection)

    if collection == 'Mentors':
        try:
            db._connect(collection).drop()
            db._connect(collection).create_index("user_id", unique=True)
            db.create_many(collection, (vars(Mentor()) for _ in range(number_records)))
        except:
            create_many(collection)

    if collection == 'Feedback':
        try:
            db._connect(collection).drop()
            db._connect(collection).create_index("ticket_id", unique=True)
            db.create_many(collection,
                           (vars(MenteeFeedback([m['user_id'] for m in mentees],
                                                [m['user_id'] for m in mentors]))
                            for _ in range(number_records)))
        except:
            create_many(collection)

if __name__ == '__main__':

    # codes from github
    db = MongoDB("UnderdogDevs")
    create_many("Mentees", 100)
    create_many("Mentors", 20)
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    create_many("Feedback", 100)
