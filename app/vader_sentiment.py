from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.api import read


vader = SentimentIntensityAnalyzer()

reviews = read('reviews')


# compound score of the sentiment
def vader_score(text: list) -> list:
    """Return compound scores of text in list using vader analysis."""
    return [vader.polarity_scores(t)["compound"] for t in text]


vader_score(reviews)
