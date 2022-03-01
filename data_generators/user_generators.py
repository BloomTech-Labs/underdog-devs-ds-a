from random import sample

from app.data import MongoDB
from data_generators.data_options import *
from app.model import MatcherSortSearch


class Mentor:

    def __init__(self):
        self.profile_id = generate_uuid(16)
        self.email = "fake@email.com"
        self.city = "Ashland"
        self.state = choice(States)
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
        self.state = choice(States)
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

'''
class Feedback:
    """Create feedback record from mentee (randomly selected from Mentees Collection) to
    mentor (randomly selected from Mentors Collection), which is stored in Feedbacks Collection.
    1 mentee can give multiple feedbacks to 1 mentor."""
    def __init__(self):
        self.mentee_id = 0
        self.mentor_id = 0
        self.ticket_id = randint(1000000, 9000000)
        self.feedback = ''
'''

def create_feedbacks():
    matched_feedbacks = []
    ticket_ids = []
    mentees = db.read("Mentees")
    mentors = db.read("Mentors")
    feedbacks_num = {'poor': 0, 'fair': 0, 'good': 0}
    while feedbacks_num['fair'] < 500 or feedbacks_num['good'] < 500:
        mentee = choice(mentees)
        random_mentors = [choice(mentors) for _ in range(randint(5,20))]
        feedback = {"mentee_profile_id": mentee['profile_id']}
        for mentor in random_mentors:
            feedback['mentor_profile_id'] = mentor['profile_id']
            if mentee["subject"] == mentor["subject"]:
                if mentee["experience_level"] == mentor["experience_level"]:
                    if mentee["pair_programming"] == mentor["pair_programming"] or mentor["industry_knowledge"]:
                        feedback['feedback'] = feedbacks[2]
                        feedbacks_num['good'] += 1
                    else:
                        feedback['feedback'] = feedbacks[1]
                        feedbacks_num['fair'] += 1
                elif mentee["pair_programming"] == mentor["pair_programming"] and mentor["industry_knowledge"]:
                    feedback['feedback'] = feedbacks[2]
                    feedbacks_num['good'] += 1
                else:
                    feedback['feedback'] = feedbacks[1]
                    feedbacks_num['fair'] += 1
            else:
                if feedbacks_num['poor'] < 500:
                    feedback['feedback'] = feedbacks[0]
                    feedbacks_num['poor'] += 1
                else:
                    continue
            feedback['ticket_id'] = randint(1000000, 9000000)
            ticket_ids.append(feedback['ticket_id'])
            matched_feedbacks.append(feedback.copy())
            if len(matched_feedbacks) == 20:
                db.create_many("Feedbacks", matched_feedbacks)
                print('feedback inserted: ', matched_feedbacks)
                matched_feedbacks = []
    db.create_many("Feedbacks", matched_feedbacks)

if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")
    '''
    db.reset_collection("Mentees")
    db.make_field_unique("Mentees", "profile_id")
    db.create_many("Mentees", (vars(Mentee()) for _ in range(200)))

    db.reset_collection("Mentors")
    db.make_field_unique("Mentors", "profile_id")
    db.create_many("Mentors", (vars(Mentor()) for _ in range(40)))
    '''
    db.get_collection("Feedbacks").drop()
    db.reset_collection("Feedbacks")
    db.make_field_unique("Feedbacks", "ticket_id")

    create_feedbacks()
    print(db.read("Mentees")[0])

