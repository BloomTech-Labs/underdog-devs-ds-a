from typing import Callable

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    analyzer = SentimentIntensityAnalyzer()

    def __call__(self, text: str) -> float:
        return self.analyzer.polarity_scores(text)["compound"]


def sentiment_analysis() -> Callable:
    analyzer = SentimentIntensityAnalyzer()

    def worker(text) -> float:
        return analyzer.polarity_scores(text)["compound"]

    return worker


sa_class = SentimentAnalyzer()
print(sa_class("Some text"))

sa_func = sentiment_analysis()
print(sa_func("Some text"))


positive = "👍"
neutral = "👌"
negative = "👎"
