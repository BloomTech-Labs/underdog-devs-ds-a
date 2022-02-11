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
    Matches potential mentors to mentee
    """

    def __init__(self):
        super(Matcher, self).__init__()

    def random_recommendations(self, N=5):
        mentors = db.read("Mentors", None)
        recommendations = list(np.random.choice(mentors, N, replace=False))
        return recommendations
