# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3.9.7 ('condenv')
#     language: python
#     name: python3
# ---

from dataclasses import dataclass, field
import random as r
import numpy as np
import pandas as p
import math as m
import itertools as iter


# ### Create mock data

# #### Class and variables

# +
@dataclass
class Mentee:
    name : str 
    need_new_comp_rank: int
    need_help_aquiring_rank: int
    

# -

# ##### name variables (long)

# +
first_names = (
    "Liam", "Noah", "Oliver", "Elijah", "William", "James", "Benjamin", "Lucas",
    "Henry", "Alexander", "Mason", "Michael", "Ethan", "Daniel", "Jacob",
    "Logan", "Jackson", "Levi", "Sebastian", "Mateo", "Jack", "Owen",
    "Theodore", "Aiden", "Samuel", "Joseph", "John", "David", "Wyatt",
    "Matthew", "Luke", "Asher", "Carter", "Julian", "Grayson", "Leo", "Jayden",
    "Gabriel", "Isaac", "Lincoln", "Anthony", "Hudson", "Dylan", "Ezra",
    "Thomas", "Charles", "Christopher", "Jaxon", "Maverick", "Josiah", "Isaiah",
    "Andrew", "Elias", "Joshua", "Nathan", "Caleb", "Ryan", "Adrian", "Miles",
    "Eli", "Nolan", "Christian", "Aaron", "Cameron", "Ezekiel", "Colton",
    "Luca", "Landon", "Hunter", "Jonathan", "Santiago", "Axel", "Easton",
    "Cooper", "Jeremiah", "Angel", "Roman", "Connor", "Jameson", "Robert",
    "Olivia", "Emma", "Ava", "Charlotte", "Sophia", "Amelia", "Isabella", "Mia",
    "Evelyn", "Harper", "Camila", "Gianna", "Abigail", "Luna", "Ella",
    "Elizabeth", "Sofia", "Emily", "Avery", "Mila", "Scarlett", "Eleanor",
    "Madison", "Layla", "Penelope", "Aria", "Chloe", "Grace", "Ellie", "Nora",
    "Hazel", "Zoey", "Riley", "Victoria", "Lily", "Aurora", "Violet", "Nova",
    "Hannah", "Emilia", "Zoe", "Stella", "Everly", "Isla", "Leah", "Lillian",
    "Addison", "Willow", "Lucy", "Paisley", "Natalie", "Naomi", "Eliana",
    "Brooklyn", "Elena", "Aubrey", "Claire", "Ivy", "Kinsley", "Audrey", "Maya",
    "Genesis", "Skylar", "Bella", "Aaliyah", "Madelyn", "Savannah", "Anna",
    "Delilah", "Serenity", "Caroline", "Kennedy", "Valentina", "Ruby", "Sophie",
    "Alice", "Gabriella", "Sadie", "Ariana", "Allison", "Hailey", "Autumn",
    "Nevaeh", "Natalia", "Quinn", "Josephine", "Sarah", "Cora", "Emery",
    "Samantha", "Piper", "Leilani", "Eva", "Everleigh", "Madeline", "Lydia",
    "Jade", "Peyton", "Brielle", "Adeline", "Vivian", "Rylee", "Clara",
    "Raelynn", "Melanie", "Melody", "Julia", "Athena", "Maria", "Liliana",
    "Hadley", "Arya", "Rose", "Reagan", "Eliza", "Adalynn", "Kaylee", "Lyla",
    "Mackenzie", "Alaia", "Isabelle", "Charlie", "Arianna", "Mary", "Remi",
    "Margaret", "Iris", "Parker", "Ximena", "Eden", "Ayla", "Kylie", "Elliana",
    "Josie", "Katherine", "Faith", "Alexandra", "Eloise", "Adalyn", "Amaya",
    "Jasmine", "Amara", "Daisy", "Reese", "Valerie", "Brianna", "Cecilia",
    "Andrea", "Summer", "Valeria", "Norah", "Ariella", "Esther", "Ashley",
    "Emerson", "Aubree", "Isabel", "Anastasia", "Ryleigh", "Khloe", "Taylor",
    "Londyn", "Lucia", "Emersyn", "Callie", "Sienna", "Blakely", "Kehlani",
)

last_names = (
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzales",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams",
    "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter",
    "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz",
    "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennet",
    "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo",
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
)


# -

def name():
    return f"{r.choice(first_names)} {r.choice(last_names)}"


# #### Create and run mock data creation function

# +
def Create_Populate_Table(Amount):
    mentees = []
    for _ in range(Amount):
        newment = Mentee(name=name(),
                         need_new_comp_rank=r.randint(0,3),
                         need_help_aquiring_rank=r.randint(0,3))
        mentees += [newment]
    return mentees
        
        
# -

menteelist = Create_Populate_Table(50)
menteelist

# #### convert to dataframe for easier manipulation 

df = p.DataFrame()
df['name'] = [x.name for x in menteelist]
df['need_new_comp_rank'] = [x.need_new_comp_rank for x in menteelist]
df['need_help_aquiring_rank'] = [x.need_help_aquiring_rank for x in menteelist]

df.head(10) 

# ### Create sorting engine, short documentation of formula and methodology

# #### Create and explain formula

# ##### Formula

# need help = x, need comp = y
#
# ${(x^2-floor(.7*x)) * (abs(y^3-y^2-y))}$

# ##### Explanation 

# **Terms**
#
# Need help or "need help aquiring rank", is a representation of how much the person needs help aquiring a computer, with 0 representing "I could buy it today no problem", 1 being "it would take a little time (1 week to 1 month)", 2 being "it would take a while (1-3 months)", 3 being "I cannot aquire on my own in any reasonable timeframe".  1 and 2 are mutable, in that they can represent different timeframes if the user wishes, but 0 and 3 are not, since they represent the extremes. The reason this is based on timeframe, instead of income, is because it takes into consideration what the person can do rather than why;  for example, someone who lives in alaska (+government stipend) is recieving aid (+some income) and has a computer building friend who has an extra build for cheap (friend discount), that person may have less overall wealth than someone who cannot free up their funds due to a looming house forclosure, but might be able to attain the new computer more quickly (due to the homeowner needing to put ALL income into debt repayment else face homelessness).
#
# Need comp or "need new computer rank", is a representation of how much the person needs a new computer, with 0 being "I do not need one at all" and 3 being "I signed up at the library and don't have a computer/ I am coding on a phone", with 1 and 2 representing values in between.  Note: 0 does not represent a "top of the line" computer, just a computer where upgrading would not improve the ability to complete the coding work.  An example: a data scientist who has to train models, may have different computing needs than someone who is developing apps for ios/android.
#
# help sort value is the value generated by the fomula from the need help and need comp values, and is how the data is sorted.  After this value is created, sorting the dataframe in descending order by this column generates the list of priorities for available computers.
#
# **Formula explanation**
#
# The formula is so that generally those who need more help aquiring are favored, since the sooner someone starts the sooner they can begin resume building, and even older computers can be worked around for learning purposes.  The exeption is when someone desperately needs a computer (rank 3), where it will be prioritized over anything else, since not having a viable computer goes from "less efficient" to "massively inefficient", or in some cases, "unable to do any learning".  If either rank is 0 (they do not need a new computer, or they do not need help aquiring), the equation zeroes out so that only someone who either needs a computer or needs help returns a positive value.

# #### Create test dataframe to ensure wanted results

a = [0,1,2,3]
b = [0,1,2,3]
c = list(iter.product(a,b))
print(c)

dftest = p.DataFrame(data=c, columns=['Need help','Need comp'])
dftest

# #### Test on test dataframe

# This will show all possible combinations of values for 'need help' and 'need comp', and the 'help sort value' generated.

col1 = dftest['Need help']
col2 = dftest['Need comp']
dftest['help sort value'] = [(x**2-m.floor((.7*x))) * (abs(y**3-y**2-y)) for x, y in zip(col1, col2)]
dftest.sort_values('help sort value', ascending=False)

mask = dftest['help sort value'] > 0
dftest[mask].sort_values('help sort value', ascending=False)

dftest.loc[dftest['help sort value'] > 0].sort_values('help sort value', ascending=False)

# #### Test on mock data

col1 = df['need_help_aquiring_rank']
col2 = df['need_new_comp_rank']
df['computer_assignment_sorting_value'] = [(x**2-m.floor((.7*x))) * (abs(y**3-y**2-y)) for x, y in zip(col1, col2)]
df.loc[df['computer_assignment_sorting_value'] > 0].sort_values('computer_assignment_sorting_value', ascending=False)
