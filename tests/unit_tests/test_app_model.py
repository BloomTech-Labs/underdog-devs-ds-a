import unittest
from unittest.mock import Mock

from app.model import MatcherSortSearch


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

    def test_matcher_output(self):
        self.assertTrue(self.test_matcher(self.test_mentee["profile_id"]))

    def test_matcher_null_mentor_field(self):
        for mentor in self.test_mentors:
            mentor.pop("pair_programming")
        with self.assertRaises(KeyError):
            self.test_matcher(self.test_mentee["profile_id"])

    def test_matcher_null_mentee_field(self):
        self.test_mentee.pop("job_help")
        with self.assertRaises(KeyError):
            self.test_matcher(self.test_mentee["profile_id"])

    def test_matcher_range_bounds(self):
        self.assertEqual(self.test_matcher(
            self.test_mentee["profile_id"], 0), [])

        self.assertIsNotNone(self.test_matcher(
            self.test_mentee["profile_id"], -10))

        self.assertEqual(len(self.test_matcher(
            self.test_mentee["profile_id"], 10)), len(self.test_mentors))


if __name__ == '__main__':
    unittest.main(verbosity=2)
