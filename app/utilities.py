from typing import Dict

# General Imports
from dataclasses import dataclass

# import for nltk
import nltk

nltk.data.path.append("./nltk_files/")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# imports from Gemsin

from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary


def dict_to_str(data: Dict) -> str:
    """Convert dictionaries into easy to read strings."""
    return "\n" + "\n".join(f"{k}: {v}" for k, v in data.items())


def financial_aid_gen(profile):
    """This is a function that queries the database
    for variables attached to a mentees profile id and applies
    that information into a formula that returns financial aid
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
        e_l = l_i + pow(9.9 * e_l, -1)
        return (e_l - 0.025) / 1.577

    return f"{f_a_func(f_i, l_i, e_l):.2%}"


def topic_function(notes, num_topic=1):
    """
    Takes a given set of notes and returns topic analysis of the given text document.
    notes: str, text document or string to get topic analysis on.
    num_topic: int, amount of topics to be returned from.
    """

    temp = []

    # custom stop word dictionary.
    stops = ['ha', 'got']

    # Lamentize and remove stop words

    for char in word_tokenize(notes):
        if char.isalpha():
            char = WordNetLemmatizer().lemmatize(char.lower())
            if char not in set(stopwords.words('english') + stops):
                temp.append(char)

    temp2 = [temp]

    # Create corpus
    corpus_dict = Dictionary(temp2)
    corpus = [corpus_dict.doc2bow(x) for x in temp2]

    # Create model
    lda = LdaModel(corpus, num_topics=num_topic,
                   random_state=69,
                   id2word=corpus_dict)
    topic = list(lda.id2word.values())

    if num_topic == 1:
        return topic[0]
    else:
        return topic[0:num_topic]

