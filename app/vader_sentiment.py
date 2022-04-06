from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


vader = SentimentIntensityAnalyzer()


def vader_score(text: str, numerical: bool):
    """Return compound scores of text in list using vader analysis."""
    score = vader.polarity_scores(text)["compound"]
    if numerical:
        return score
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"


if __name__ == '__main__':
    print(vader_score("good but not great", False))
    """
    This is to test the expected result requested in api.py

    """
    # Numeric
    print({"Result": vader_score("Astring is so cool wow hot damn", True)})
    # String text.
    print({"Result": vader_score("Astring is so cool wow hot damn", False)})

