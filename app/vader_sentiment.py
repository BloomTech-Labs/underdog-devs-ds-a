from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def vader_score(text: str):
    """
    Returns vader scores for feedback
    """
    score = analyzer.polarity_scores(text)['compound']
    return score


if __name__ == '__main__':
    """
    This is to test the expected result requested in api.py
    """

    print({"Result": vader_score("A string is so cool wow, I hope this is a positive.")})
