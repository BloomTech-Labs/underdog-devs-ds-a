from typing import List, Union

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


vader = SentimentIntensityAnalyzer()


def vader_score(text: str) -> list[Union[str, int]]:
    """Return compound scores of text in list using vader analysis."""
    score = vader.polarity_scores(text)["compound"]
    if score > 0.3:
        return ["Positive", 1]
    elif score < -0.3:
        return ["Negative", -1]
    else:
        return ["Neutral", 0]


if __name__ == '__main__':
    print(vader_score("good but not great"))
    # print(vader_score("A line of strings is only as good as a number"))
    """
    This is to test the expected result requested in api.py
    
    """
    print({"Result": vader_score("Astring is so cool wow hot damn")[1]})
    print({"Result": vader_score("Astring is so cool wow hot damn")[0]})