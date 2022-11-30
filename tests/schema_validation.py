from uuid import uuid4

from app.schema import Feedback, Meeting, Mentee, Mentor
from data_generators.generators import (RandomMeeting,
                                        RandomMentee,
                                        RandomMenteeFeedback,
                                        RandomMentor)


def validate_mentor():
    assert all(Mentor(**vars(RandomMentor())) for _ in range(1000))


def validate_mentee():
    assert all(Mentee(**vars(RandomMentee())) for _ in range(1000))


def validate_meeting():
    assert all(
        Meeting(**vars(RandomMeeting(
            str(uuid4()),
            str(uuid4()),
        )))
        for _ in range(1000)
    )


def validate_feedback():
    assert all(
        Feedback(**vars(RandomMenteeFeedback(
            str(uuid4()),
            str(uuid4()),
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
