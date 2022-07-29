import inspect
from app.schema import *
from data_generators.generators import *

def validate_mentor():
    # compare shapes
    length1 = 0
    length2 = 0
    mentor = Mentor()
    randomMentor = RandomMentor()
    for i in range(len(inspect.getmembers(mentor)[2][1]:
        length1 += 1
    for i in range(len(inspect.getmembers(randomMentor)[2][1]:
        length2 += 1

    assert length1 == length2, "collections don't match"


def validate_mentee():
    # compare shapes
    length1 = 0
    length2 = 0
    mentee = Mentee()
    randomMentee = RandomMentee()
    for i in range(len(inspect.getmembers(mentee)[2][1]:
        length1 += 1
    for i in range(len(inspect.getmembers(randomMentee)[2][1]:
        length2 += 1

    assert length1 == length2, "collections don't match"

def validate_meeting():
    # compare shapes
    length1 = 0
    length2 = 0
    meeting = Meeting()
    randomMeeting = RandomMeeting()
    for i in range(len(inspect.getmembers(meeting)[2][1]:
        length1 += 1
    for i in range(len(inspect.getmembers(randomMeeting)[2][1]:
        length2 += 1

    assert length1 == length2, "collections don't match"

def validate_feedback():
    # compare shapes
    length1 = 0
    length2 = 0
    feedback = Feedback()
    randomFeedback = RandomMenteeFeedback()
    for i in range(len(inspect.getmembers(feedback)[2][1]:
        length1 += 1
    for i in range(len(inspect.getmembers(randomFeedback)[2][1]:
        length2 += 1

    assert length1 == length2, "collections don't match"

'''length = 0
mentor = Mentor
for i in inspect.getmembers(mentor):
    length += 1

#print(length)

print(len(inspect.getmembers(mentor)[2][1]))'''