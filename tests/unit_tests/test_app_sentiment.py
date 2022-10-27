import unittest

from app.sentiment import sentiment_score, sentiment_rank, apply_sentiment


class TestSentiment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize environment for test suite"""
        cls.text_positive = "Wow! This is super!"
        cls.text_negative = "Very disappointed. Bad quality!"
        cls.text_neutral = "No opinion"
        cls.text_null = ""
        cls.text_num = "-12345.50"

    def test_sentiment_score_input(self):
        self.assertIsInstance(sentiment_score(self.text_null), float)
        self.assertIsInstance(sentiment_score(self.text_num), float)
        self.assertIsInstance(sentiment_score(self.text_neutral), float)

    def test_sentiment_rank_sentiments(self):
        self.assertEqual(sentiment_rank(self.text_positive), "Positive")
        self.assertEqual(sentiment_rank(self.text_negative), "Negative")
        self.assertEqual(sentiment_rank(self.text_neutral), "Neutral")

    def test_apply_sentiment_update(self):
        with self.assertRaises(KeyError): apply_sentiment({})
        self.assertIn("sentiment", apply_sentiment({"text": self.text_neutral}).keys())


if __name__ == '__main__':
    unittest.main(verbosity=2)
