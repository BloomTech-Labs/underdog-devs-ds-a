from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

# compound score of the sentiment
def vader_score(text: list) -> list:

    return [vader.polarity_scores(t)["compound"] for t in text]
