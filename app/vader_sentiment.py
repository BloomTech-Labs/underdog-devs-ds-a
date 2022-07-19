from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()


def vader_score(text: str):
    """
    Return an intuitive string
    (Positive, Negative or Neutral)
    base on the compound score of text from vader analysis.
    """
    score = vader.polarity_scores(text)["compound"]
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"


def vader_compound_score(text: str):
    """
    Gets the compound vader score.
    For use with feedback graphs.
    """
    return vader.polarity_scores(text)["compound"]


if __name__ == '__main__':
    """
    This is to test the expected result requested in api.py
    """

    print({"Result": vader_score("A string is so cool wow, I hope this is a positive.")})
