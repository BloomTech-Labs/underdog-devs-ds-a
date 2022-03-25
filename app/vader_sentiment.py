from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


vader = SentimentIntensityAnalyzer()


def vader_score(text: str) -> str:
    """Return compound scores of text in list using vader analysis."""
    score = vader.polarity_scores(text)["compound"]
    if score > 0.45:
        return "Positive"
    elif score < -0.45:
        return "Negative"
    else:
        return "Neutral"


if __name__ == '__main__':
    print(vader_score("This is really good but not perfect"))
