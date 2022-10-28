import unittest

from app.api import API


class TestAPISetup(unittest.TestCase):

    def test_api_attributes(self):
        self.assertIsNotNone(API)
        attr = vars(API)
        self.assertIsNotNone(API.db)
        self.assertIn("version", attr.keys())
        self.assertIn("title", attr.keys())
        self.assertTrue(API.router.routes)
        self.assertTrue(attr['user_middleware'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
