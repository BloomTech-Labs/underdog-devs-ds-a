import spacy
from collections import Counter


def nlp_analysis(user_responses):
    """Returns relevant topics
    
    takes responses performs nlp analysis
    
    Returns:
    unordered (dict)topics from mentee responses collection
  
    """

    nlp = spacy.load("en_core_web_sm")

    responses_list = []
    for word in user_responses:
        for token in nlp(word):
            if token.pos_ in ('ADJ', 'VERB', 'NOUN'):
                responses_list.append(token.lemma_.lower())

    return dict(Counter(responses_list))


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
