from typing import Dict


# import for nltk
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# imports from Gemsin
from gensim.models.ldamodel import Ldamodel
from gensim.corpora.dictionary import Dictionary.

def dict_to_str(data: Dict) -> str:
    """Convert dictionaries into easy to read strings."""
    return "\n" + "\n".join(f"{k}: {v}" for k, v in data.items())


def financial_aid_gen(profile):
    """This is a function that queries the database
    for variables attached to a mentees profile id and applies
    that information into a forumla that returns financial aid
    probability"""

    e_l_dict = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
    f_i = (1 if profile['formerly_incarcerated'] else 0)
    l_i = 1 if profile['low_income'] else 0
    e_l = e_l_dict[profile['experience_level']]

    def f_a_func(f_i, l_i, e_l):
        """Algorithm (from McGraw_Papenburg.ipynb)
        This can be modified to include future Mentee
        database variables"""

        f_i /= 2
        l_i += f_i
        e_l = l_i + pow(9.9*e_l, -1)
        return (e_l - 0.025) / 1.577

    return f"{f_a_func(f_i, l_i, e_l):.2%}"
#nltk.data.path.append("./nltk_files")