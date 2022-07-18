from random import choice

from app.data import MongoDB
from data_generators.generators import *


class SeedMongo:
    db = MongoDB("UnderdogDevs")

    def mentees(self, fresh_db: bool, count: int):
        if not fresh_db:
            self.db.delete("Mentees", {})
            self.db.drop_index("Mentees")
        else:
            self.db.make_field_unique("Mentees", "profile_id")
        self.db.create_index("Mentees")
        mentees = (vars(RandomMentee()) for _ in range(count))
        self.db.create_many("Mentees", mentees)

    def mentors(self, fresh_db: bool, count: int):
        if not fresh_db:
            self.db.delete("Mentors", {})
            self.db.drop_index("Mentors")
        else:
            self.db.make_field_unique("Mentors", "profile_id")
        self.db.create_index("Mentors")
        mentors = (vars(RandomMentor()) for _ in range(count))
        self.db.create_many("Mentors", mentors)

    def feedback(self, fresh_db: bool, count: int):
        mentees = self.db.read("Mentees")
        mentors = self.db.read("Mentors")
        if not fresh_db:
            self.db.delete("Feedback", {})
        else:
            self.db.make_field_unique("Feedback", "ticket_id")
        feedback = (vars(RandomMenteeFeedback(
            choice(mentees)["profile_id"],
            choice(mentors)["profile_id"],
        )) for _ in range(count))
        self.db.create_many("Feedback", feedback)

    def meetings(self, fresh_db: bool, count: int):
        mentees = self.db.read("Mentees")
        mentors = self.db.read("Mentors")
        if not fresh_db:
            self.db.delete("Meetings", {})
        else:
            self.db.make_field_unique("Meetings", "meeting_id")
        meetings = (vars(RandomMeeting(
            choice(mentees)["profile_id"],
            choice(mentors)["profile_id"],
        )) for _ in range(count))
        self.db.create_many("Meetings", meetings)

    def resources(self, fresh_db: bool, count: int):
        if not fresh_db:
            self.db.delete("Resources", {})
        else:
            self.db.make_field_unique("Resources", "item_id")
        resources = (vars(RandomResource()) for _ in range(count))
        self.db.create_many("Resources", resources)

    def __call__(self, fresh: bool):
        self.mentees(fresh, 100)
        self.mentors(fresh, 20)
        self.feedback(fresh, 50)
        self.meetings(fresh, 150)
        self.resources(fresh, 10)


if __name__ == '__main__':
    seed_mongo = SeedMongo()
    seed_mongo(fresh=False)
