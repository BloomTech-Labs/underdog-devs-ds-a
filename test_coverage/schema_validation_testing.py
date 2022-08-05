from app.schema import Mentor, Mentee, Meeting, Feedback
from data_generators.generators import RandomMentor, RandomMentee, RandomMeeting, RandomMenteeFeedback
from data_generators.data_options import generate_uuid


def test_mentor():
    for _ in range(1000):
        assert all(Mentor(**vars(RandomMentor())))


def test_mentee():
    mentee = RandomMentee()
    for _ in range(1000):
        assert all(Mentee(**vars(RandomMentee())))


def test_meeting():
    meeting = RandomMeeting(generate_uuid(16), generate_uuid(16))
    for _ in range(1000):
        assert all(Meeting(**vars(RandomMeeting())))



def test_feedback():
    feedback = RandomMenteeFeedback(generate_uuid(16), generate_uuid(16))
    for _ in range(1000):
        assert all(MenteeFeedback(**vars(RandomMenteeFeeback())))


def test_collections():
    test_mentor()
    test_mentee()
    test_meeting()
    test_feedback()


if __name__ == '__main__':
    test_collections()
