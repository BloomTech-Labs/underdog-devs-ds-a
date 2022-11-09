import unittest

from app.graphs import title_fix


class TestGraphs(unittest.TestCase):

    def test_title_fix_output(self):
        test_title, test_title_fixed = "This_is_text!", "This Is Text!"

        self.assertEqual(title_fix(test_title), test_title_fixed)
        self.assertEqual(title_fix(test_title_fixed), test_title_fixed)
        self.assertEqual(title_fix(""), "")


if __name__ == '__main__':
    unittest.main(verbosity=2)
