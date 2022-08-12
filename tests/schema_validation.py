from app.schema import Mentor, Mentee, Meeting, Feedback
from data_generators.generators import RandomMentor, RandomMentee
from data_generators.generators import RandomMeeting, RandomMenteeFeedback
from data_generators.data_options import generate_uuid


def validate_mentor():
    assert all(Mentor(**vars(RandomMentor())) for _ in range(1000))


def validate_mentee():
    assert all(Mentee(**vars(RandomMentee())) for _ in range(1000))


def validate_meeting():
    assert all(
        Meeting(**vars(RandomMeeting(
            generate_uuid(16),
            generate_uuid(16),
        )))
        for _ in range(1000)
    )


def validate_feedback():
    assert all(
        Feedback(**vars(RandomMenteeFeedback(
            generate_uuid(16),
            generate_uuid(16),
        )))
        for _ in range(1000)
    )


def validate_schemas():
    validate_mentor()
    validate_mentee()
    validate_meeting()
    validate_feedback()


if __name__ == '__main__':
    validate_schemas()
