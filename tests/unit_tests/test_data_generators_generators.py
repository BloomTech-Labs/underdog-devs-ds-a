# Hack if you have problems with import:
#
# import os
#
# os.chdir("../../")

import unittest
from datetime import datetime

from data_generators.generators import percent_true, RandomMentee, RandomMentor, RandomMenteeFeedback, RandomMeeting, \
    random_first_name, random_datetime


class TestRandomFunctions(unittest.TestCase):

    def test_percent_true(self):
        self.assertTrue(percent_true(110))
        self.assertFalse(percent_true(0))

    def test_random_first_name(self):
        first_name = random_first_name(50)
        self.assertIsInstance(first_name, str)

    def test_random_datetime(self):
        rnd_datetime = random_datetime(datetime(2022, 1, 1), datetime(2022, 12, 31))
        self.assertIsInstance(rnd_datetime, datetime)

    def test_failed_random_datetime(self):
        with self.assertRaises(ValueError):
            random_datetime(datetime(2023, 1, 1), datetime(2022, 12, 31))

# Tests that we don't really need

    def test_create_random_mentee(self):
        result = vars(RandomMentee())
        self.assertEqual(result['country'], 'U.S.')

    def test_create_random_mentor(self):
        result = vars(RandomMentor())
        self.assertIn(result['validate_status'], ["approved", "pending"])

    def test_create_random_mentee_feedback(self):
        result = vars(RandomMenteeFeedback(1, 2))
        self.assertTrue(len(result['text']) > 0)

    def test_create_random_meeting(self):
        result = vars(RandomMeeting(1, 2))
        self.assertEqual(result['admin_meeting_notes'], "Meeting notes here!")


if __name__ == '__main__':
    unittest.main()
