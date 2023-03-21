from random import choice

from app.data import MongoDB
from data_generators.generators import RandomMentee, RandomMentor
from tests.schema_validation import validate_schemas


class SeedMongo:
    validate_schemas()
    db = MongoDB()

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

    def make_matches(self):
        mentees = tuple(self.db.collection("Mentees").find({}, {"_id": False}))
        mentors = tuple(self.db.collection("Mentors").find({}, {"_id": False}))
        for mentee in mentees:
            mentor_id = choice(mentors).get("profile_id")
            mentee_id = mentee.get("profile_id")
            self.db.collection("Mentees").update_one(
                {"profile_id": mentee_id},
                {"$addToSet": {"matches": mentor_id}},
            )
            self.db.collection("Mentors").update_one(
                {"profile_id": mentor_id},
                {"$addToSet": {"matches": mentee_id}},
            )

    def __call__(self, fresh: bool):
        self.mentees(fresh, 100)
        self.mentors(fresh, 20)
        self.make_matches()


if __name__ == '__main__':
    seed_mongo = SeedMongo()
    seed_mongo(fresh=True)
