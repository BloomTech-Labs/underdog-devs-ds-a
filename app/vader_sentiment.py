from typing import Callable

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    analyzer = SentimentIntensityAnalyzer()

    def __call__(self, text: str) -> float:
        return self.analyzer.polarity_scores(text)["compound"]


sa_class = SentimentAnalyzer()
print(sa_class("Some text"))


positive = "👍"
neutral = "👌"
negative = "👎"
