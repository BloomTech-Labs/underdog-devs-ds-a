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
    '''
    # codes from github
    db = MongoDB("UnderdogDevs")

    db.reset_collection("Mentees")
    #db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))

    db.reset_collection("Mentors")
    #db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))
    '''
    import random
    from os import getenv
    from pymongo import MongoClient
    from dotenv import load_dotenv
    import certifi

    load_dotenv()


    def create_Mentees():
        #create data for Mentees
        connection = MongoClient(getenv("MONGO_URL"), tlsCAFile=certifi.where())["UnderdogDevs"]["Mentees"]
        mentees_list = [
            {
                'user_id': random.randint(1000000, 9000000),
                'last_name': random.choice(last_names),
                'user_type': 'Mentee',
                'subject': random.choice(subjects),
                'skill_level': random.choice(skill_levels),
                'feedback': random.choice(feedbacks)
            }
            for _ in range(100)]
        connection.drop()
        connection.insert_many(mentees_list)


    def create_Mentors():
        connection = MongoClient(getenv("MONGO_URL"), tlsCAFile=certifi.where())["UnderdogDevs"]["Mentors"]
        mentors_list = [
            {
                'user_id': random.randint(1000000, 9000000),
                'last_name': random.choice(last_names),
                'user_type': 'Mentor',
                'subject': random.choice(subjects),
                'skill_level': random.choice(skill_levels)
            }
            for _ in range(20)]
        connection.drop()
        connection.insert_many(mentors_list)


    if __name__ == '__main__':
        db = MongoDB('UnderdogDevs')
        create_Mentees()
        create_Mentors()
