# Hack if you have problems with import:
#
# import os
#
# os.chdir("../../")

import unittest
from datetime import datetime

from data_generators.generators import percent_true, random_first_name, random_datetime


class TestRandomFunctions(unittest.TestCase):

    def test_percent_true(self):
        self.assertTrue(percent_true(110))
        self.assertFalse(percent_true(0))
        self.assertFalse(percent_true(-100))
        self.assertIsInstance(percent_true(1000), int)

    def test_failed_percent_true(self):
        with self.assertRaises(TypeError):
            percent_true('String')

    def test_random_first_name(self):
        self.assertIsInstance(random_first_name(50), str)
        # random_first_name return a random value, so we can't test it much, all our test will repeat test_percent_true

    def test_random_datetime(self):
        rnd_datetime = random_datetime(datetime(2022, 1, 1), datetime(2022, 12, 31))
        self.assertIsInstance(rnd_datetime, datetime)
        self.assertGreater(rnd_datetime, datetime(2022, 1, 1))
        self.assertLess(rnd_datetime, datetime(2022, 12, 31))


    def test_failed_random_datetime(self):
        with self.assertRaises(ValueError):
            random_datetime(datetime(2023, 1, 1), datetime(2022, 12, 31))


if __name__ == '__main__':
    unittest.main()
