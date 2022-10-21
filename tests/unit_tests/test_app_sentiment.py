import unittest
from app.sentiment import sentiment_rank


class TestSentiment(unittest.TestCase):
    def test_sentiment_score(self):
        text_positive = "Wow! This is super!"
        text_negative = "Very disappointed. Bad quality!"
        self.assertEqual(sentiment_rank(text_positive), "Positive")
        self.assertEqual(sentiment_rank(text_negative), "Negative")


if __name__ == '__main__':
    unittest.main()
