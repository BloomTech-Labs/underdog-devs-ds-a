"""
Labs DS Machine Learning Engineer Role
- Machine Learning Model Interface
"""
from sklearn.metrics.pairwise import cosine_similarity
from app.data import MongoDB
import pandas as pd
import numpy as np
import json


class Matcher:
    """Documentation for Matcher
    A class used to represent a Matcher. Matches a mentor and mentee.

    ...

    Attributes
    ----------

    Methods
    -------
    random_recommendations(N=5)
        returns N mentors randomly
    """

    def __init__(self, db):
        self.db = db

    def random_recommendations(self, N=5):
        """
        Reads all mentors in db, then returns a list of length N random mentors

        Parameters
        ----------
            N : int
                number of recommendations to return
        """
        mentors = self.db.dataframe("Mentors")
        recommendations = mentors.iloc[
            np.random.choice(range(len(mentors)), N, replace=False)
        ]

        return recommendations.to_dict(orient="records")


if __name__ == "__main__":
    db = MongoDB("UnderdogDevs")
    matcher = Matcher(db)
    assert len(matcher.random_recommendations(3)) == 3
