"""
Labs DS Machine Learning Engineer Role
- Machine Learning Model Interface
"""
from sklearn.metrics.pairwise import cosine_similarity
from app.data import MongoDB
import pandas as pd
import numpy as np


db = MongoDB("UnderdogDevs")


class Matcher(object):
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

    def __init__(self):
        super(Matcher, self).__init__()

    def random_recommendations(self, N=5):
        """
        Reads all mentors in db, then returns a list of length N random mentors

        Parameters
        ----------
            N : int
                number of recommendations to return
        """
        mentors = db.read("Mentors", None)
        recommendations = list(np.random.choice(mentors, N, replace=False))
        return recommendations
