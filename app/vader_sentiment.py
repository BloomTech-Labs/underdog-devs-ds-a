from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

# compound score of the sentiment
def vader_score(text: list) -> list:
    """Return compound scores of text in list using vader analysis."""
    return [vader.polarity_scores(t)["compound"] for t in text]
