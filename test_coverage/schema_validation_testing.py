from app.schema import Mentor, Mentee, Meeting, Feedback
from data_generators.generators import RandomMentor, RandomMentee, RandomMeeting, RandomMenteeFeedback
from data_generators.data_options import generate_uuid



def test_mentor():
    mentor = RandomMentor()
    mentor_dict = vars(mentor)

    assert Mentor(**mentor_dict)


def test_mentee():
    mentee = RandomMentee()
    mentee_dict = vars(mentee)

    assert Mentee(**mentee_dict)


def test_meeting():
    meeting = RandomMeeting(generate_uuid(16), generate_uuid(16))
    meeting_dict = vars(meeting)

    assert Meeting(**meeting_dict)


def test_feedback():
    feedback = RandomMenteeFeedback(generate_uuid(16), generate_uuid(16))
    feedback_dict = vars(feedback)
    Feedback(**feedback_dict)

    assert Feedback(**feedback_dict)


def test_collections():
    test_mentor()
    test_mentee()
    test_meeting()
    test_feedback()


if __name__ == '__main__':
    test_collections()
