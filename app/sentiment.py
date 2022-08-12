from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()


def sentiment_score(text: str) -> float:
    return vader.polarity_scores(text)["compound"]


def sentiment_rank(text: str) -> str:
    score = sentiment_score(text)
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"
