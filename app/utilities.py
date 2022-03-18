from typing import Dict


def dict_to_str(data: Dict) -> str:
    """Convert dictionaries into easy to read strings."""
    return "\n" + "\n".join(f"{k}: {v}" for k, v in data.items())


def financial_aid_gen(profile):
    """This is a function that queries the database
    for variables attached to a mentees profile id and applies
    that information into a forumla that returns financial aid
    probability"""

    E_l_dict = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
    formerly_incarcerated = (1 if profile['formerly_incarcerated'] == 'true'
                             else 0)
    low_income = 1 if profile['low_income'] == 'true' else 0
    experience_level = E_l_dict[profile['experience_level']]

    return (((formerly_incarcerated/2 + low_income +
              pow(9.9*(experience_level), -1) - 0.025) / 1.577))
