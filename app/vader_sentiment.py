from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


vader = SentimentIntensityAnalyzer()


def vader_score(text: str) -> str:
    """Return compound scores of text in list using vader analysis."""
    score = vader.polarity_scores(text)["compound"]
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"


if __name__ == '__main__':
    print(vader_score("good but not great"))
