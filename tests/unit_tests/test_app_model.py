import unittest
from unittest.mock import Mock

from app.model import *


class TestMatcherSortSearch(unittest.TestCase):

    def setUp(self):
        """Initialize object(s) before each test case"""
        self.test_matcher = MatcherSortSearch()
        self.test_mentee = {"profile_id": "test_mentee_id_0",
                            "tech_stack": None,
                            "pair_programming": None,
                            "job_help": None}
        self.test_mentors = [{"profile_id": ("test_mentor_id_" + str(x)),
                              "tech_stack": None,
                              "pair_programming": None,
                              "job_help": None,
                              "industry_knowledge": None} for x in range(5)]
        self.test_matcher.db.first = Mock()
        self.test_matcher.db.first.return_value = self.test_mentee
        self.test_matcher.db.read = Mock()
        self.test_matcher.db.read.return_value = self.test_mentors

    def test_matcher_null_fields(self):
        self.assertIsNotNone(self.test_matcher(self.test_mentee["profile_id"]))

        bad_mentors = self.test_mentors.copy()
        for mentor in bad_mentors:
            mentor.pop("pair_programming")
        self.test_matcher.db.read.return_value = bad_mentors
        with self.assertRaises(KeyError):
            self.test_matcher(self.test_mentee["profile_id"])

        bad_mentee = self.test_mentee.copy()
        bad_mentee.pop("job_help")
        self.test_matcher.db.first.return_value = bad_mentee
        self.test_matcher.db.read.return_value = self.test_mentors
        with self.assertRaises(KeyError):
            self.test_matcher(self.test_mentee["profile_id"])

    def test_matcher_range_bounds(self):
        self.assertEqual(self.test_matcher(self.test_mentee["profile_id"], 0), [])

        self.assertIsNotNone(self.test_matcher(self.test_mentee["profile_id"], -10))

        self.assertEqual(len(self.test_matcher(self.test_mentee["profile_id"], 10)), len(self.test_mentors))


if __name__ == '__main__':
    unittest.main(verbosity=2)
