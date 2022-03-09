# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# + [markdown] id="-RoCPG84Ywl6"
# # To help mentees narrow down the scope of interest that each likes to learn for tech job, first each mentee reads the 12 types of software engineer job function(the URL link below), and the mentee narrows down one type as career goal. Then, match the mentee with career goal in mind with a mentor who has knowledge to offer advice on programs to learn.
#
# The webpage shown the languages to learn for each job type --
# 12 Types of Software Engineers To Help You Find Your Place in Technology: 
# https://www.indeed.com/career-advice/finding-a-job/types-of-software-engineer
#
# # After mentee and mentor match, then the mentee could schedule a meeting with a mentor on Calendly for advice.

# + id="lsgbujRhdjIc"
# dataset, each mentee with one career goal selected

mentees = [
    {
        "name": "Michael",
        "career goal": "video game designer",
    },
    {
        "name": "Jack",
        "career goal": "full-stack engineer"
    }

]

# + id="skXlO4jIgHdk"
# each mentor may be offering more than one scope of interest for advice

mentors = [
    {
        "name": "Louis",
        "scope of interest": ["video game designer", "quality assurance engineer", "CRM project manager"]
    },
    {
        "name": "Kenny",
        "scope of interest": ["full-stack engineer", "software integration engineer", "security engineer"]
    }
]

# + id="kP3E49q4kRX-"
# for loop to match each mentee with one career goal with mentor
for mentee in mentees:
  for mentor in mentors:
    if mentee["career goal"] in mentor["scope of interest"]:
      print(mentee["name"], "->", mentor["name"])

# + [markdown] id="6C_6c5MzlHY7"
# After mentee and mentor match, then the mentee could schedule a meeting with a mentor on Calendly.
