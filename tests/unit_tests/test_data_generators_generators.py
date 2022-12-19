from datetime import datetime
import unittest

from data_generators.generators import (percent_true,
                                        random_datetime,
                                        random_first_name)


class TestRandomizerFunctions(unittest.TestCase):

    def test_percent_true_input(self):
        self.assertFalse(percent_true(-100))
        self.assertTrue(percent_true(1000))

        with self.assertRaises(TypeError):
            percent_true('String')

    def test_percent_true_output(self):
        self.assertIsInstance(percent_true(50), bool)
        self.assertTrue(percent_true(100))
        self.assertFalse(percent_true(0))

    def test_random_first_name_output(self):
        self.assertIsInstance(random_first_name(50), str)
        self.assertNotEqual(random_first_name(50), "")

    def test_random_datetime_output(self):
        rnd_datetime = random_datetime(
            datetime(2022, 1, 1), datetime(2022, 12, 31))
        self.assertIsInstance(rnd_datetime, datetime)
        self.assertGreater(rnd_datetime, datetime(2022, 1, 1))
        self.assertLess(rnd_datetime, datetime(2022, 12, 31))

    def test_random_datetime_input(self):
        with self.assertRaises(ValueError):
            random_datetime(datetime(2023, 1, 1), datetime(2022, 12, 31))


if __name__ == '__main__':
    unittest.main(verbosity=2)
