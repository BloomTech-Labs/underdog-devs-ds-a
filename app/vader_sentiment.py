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


def vader_numeric(text: str) -> float:
    """
    Return numeric 'compound' score of text using vader analysis.
    :param text: Input text (as string)
    :return: float representing the Vader sentiment analysis' "Compound" score,
    representing the overall sentiment of the words in the text string. Note
    that the compound score values range from -1 (100% negative) to +1 (100%
    positive).
    """
    return vader.polarity_scores(text)["compound"]


if __name__ == '__main__':
    print(vader_score("good but not great"))
