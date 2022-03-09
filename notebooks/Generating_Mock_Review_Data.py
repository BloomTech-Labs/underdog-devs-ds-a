# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: underdog
#     language: python
#     name: underdog
# ---

# + [markdown] id="koqy3Y5hXhfs"
# ## Generating mock review data where mentor gives review to mentee

# + [markdown] id="z7F1rIxsepNL"
# ## Generating mock review Data

# + id="BnaL5IirXbFg"
import pandas as pd
import random as r

# +
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

# compound score of the sentiment
def vader_score(text: list) -> list:
    """Return compound scores of text in list using vader analysis."""
    return [vader.polarity_scores(t)["compound"] for t in text]


# + id="YtOeMNNOYRp_"
df = pd.read_csv('review.csv')

# + colab={"base_uri": "https://localhost:8080/", "height": 424} id="3HKHnLVSY-hz" outputId="4b1d4ce6-0ae5-4b17-8020-27cd54849e28"
df.drop(columns=['Id','Label'],inplace=True)
df

# + [markdown] id="8rQQR7ZDeTVh"
# ## Adding Mentee And Mentor ID's Mock Data to the data frame

# + id="hEKLqbVqY--t"
df['mentor_id'] =["O" + str(hash(r.randint(2000000, 70000000000000000))) for _ in range(df.shape[0]) ]

# + id="T05YqjGAd7aL"
df['mentee_id'] = ["E" + str(r.randint(1000000, 70000000000000)) for _ in range(df.shape[0])]

# + colab={"base_uri": "https://localhost:8080/", "height": 424} id="3av4tswbd73i" outputId="473eb396-33d1-4c8e-e3d9-02bd4cbeb185"
df


# -

def one_vader_score(text):
    return vader.polarity_scores(text)['compound']


df['Review'].apply(one_vader_score)


df["compound_score"] = df['Review'].apply(one_vader_score)

df.head()


def is_positive(number):
    if number >= 0.05:
        return 1
    else:
        return 0


df['positive'] = df['compound_score'].apply(is_positive)

df.head()

df['positive'].value_counts()

df.to_csv('reviews_with_sentiment.csv', encoding = 'utf-8')


