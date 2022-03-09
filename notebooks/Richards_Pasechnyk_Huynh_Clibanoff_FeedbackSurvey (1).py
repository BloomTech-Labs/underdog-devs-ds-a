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

# + [markdown] id="YK4ZWJmzJ2k8"
# #Spring Board for post-meeting feedback

# + id="xDou3a7vNNie"
#Import Libraries
import random as r
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# + [markdown] id="53AznKD0BAaR"
# ### Mentees who receive financial aid might have more strict requirements so knowing if they show up and if they're doing their work might be a priority to consider
#

# + id="jQ3YQpcf-l3E"
#Potential Reference for metrics
Mentor = "https://uwmadison.co1.qualtrics.com/jfe/form/SV_ah3sUnFOUNJouDX?Q_JFE=qdg"
Mentee = "https://uwmadison.co1.qualtrics.com/jfe/form/SV_9vEPVJ9H0ksWEPr?Q_JFE=qdg"
Both_sentiment = "https://www.aquinas.edu/alumni/events-and-volunteer-opportunities/aq-alumni-mentorship-network-program/mentoring-program"

# + [markdown] id="hRL9e2MVv1fx"
# #Questions that could be asked

# + [markdown] id="CLEY5CR3DEp5"
# Did the mentee show up? \
# Did the mentee come prepared? \
# Has the mentee completed homework outside of mentor hours? \
# Is the mentee showing marked improvement?
#   - These seem to be a core metric: perhaps the more often these are true, the more often the student will be successful? Are there certain features from the above four that are more important than others?
#
# How would you rate the mentee's current skills? 
#   - (Beginner, Intermediate, Advanced)
#   - A professional opinion on their skills could change the weight of certain skills.  
#
# Is the mentee looking to improve his technical skills, career readiness skills, life skills or all of the above? \
#   - *If certain skills fall into these categories we need to know. If they show proficiency in one area and not in another we need to be aware of whether or not the mentor they are currently with is the best use of resources for underdog devs and/or the best match for the mentee* \
#
# Are there any roadblocks to mentee success?
#
# Other:
#
# Other notes for the mentee \
# Other notes for future mentors \
#
#
# What is the Mentee's timeline? (i.e. if they're in a bootcamp how long etc) \

# + [markdown] id="GOcDwzGe6wEn"
# #Why and Ideas

# + [markdown] id="GZKyR-3W6zxg"
# What do we think the surveys will help with? 
#   - I want to know if they're **showing up prepared**.
#     - This tells the mentor and underdog devs that their time is respected
#   - I want to know what their mentor makes of their **skill rank**
#     - this will tell how ready they are to move on from this mentor or start applying
#   - I want to know if their skill requirements are being met with their current mentor. **Soft skills** may be especially pertinent here.
#     - based on changes in skill levels and categories in which those skill levels are, is the mentor's skill group being effectively leveraged?
#      - For example: Tech mentor has seen tech/career mentee to 'python', 'R' advancement and now mentee needs career/life coach. If another mentee comes along who needs Python but not career/life coaching, having some kind of notice that mentor is potentially available could be good. 
#   - What other factors might influence success? 
#     - Are they receiving **financial assistance**?
#     - Do they have a **pair-programming buddy**? 
#       - This could be a good idea ^-^ 
#       - checks and balances to ensure one isn't doing more work/other's work
#       - Stretch goal for sure but something to run by stakeholder
#     - What do they do when they run into issues with coding? 
#       - options: stop, 20 min then break, request resources (from who?)??
#     - Does mentee have clear expectations for the week? 

# + [markdown] id="FlsviVrLYjRo"
# # Future tasks: 

# + [markdown] id="MlzwR7pREY5r"
# ##link to exit survey \
#   - was the mentee successful? (feedback for milestones) \
#     - If mentees are successful, what measured data do we have regarding the milestones that they hit. Did showing up regularly lead to success? Did doing homework consistently lead to success? Etc. \
#
#   - was the match successful? (feedback for matching algo) \
#     - how to measure this? Perhaps mentee/mentor subjective satisfaction? Long term contact? 
#   - was the mentor successful? (consistent mentee failure?) \
#     - If the mentor has enough mentee's fail, perhaps sending tickets to admins as a sort of redflag? They could then consult feedback forms? \

# + [markdown] id="fRKXdmtnHpnk"
# ### Should we have a form to check for understanding on the part of the mentee? Do the mentors want feedback? 

# + [markdown] id="fJK_mLH7JNYA"
# As mentee, do you have a clear understanding of your tasks for the week? \
#
# Do you feel like you're improving as a programmer? \
#
#

# + [markdown] id="n7lFCC0xMCgr"
# # List of choices for questions

# + id="3sZmIgGrMB42"
exp_level = (
    "Beginner", "Intermediate", "Advanced",
)

purpose = (
    "Technical", "Career Preparation", "Life Coaching"
)

roadblocks = (
    "financial", "interpersonal", "housing", "time_management",
    "learning_resources", "learning_strategies" "computer_or_wifi access", "more_mentor_time",
    "building_routine", "presentation_professionalism", "community", "none"
)

industry = (
    "unsure", "health_and_wellness", "data_storage_and_security", "customer_relationship_management", "travel", "accounting_and_finance",
    "application_and_data_integration", "human_resources_and_workforce_management", "supply_chain_and_logistics", "food_and_grocery",
    "web_development", "lighting_and_LED", "infrastructure_and_hosting", "collaboration_and_project_management", "data_and_broadband",
    "music", "real_estate")

financial_aid = ("Yes", "No")
showup = ("showed_up", "no_show")
prepared = ("prepared", "not_prepared")
homework = ("complete", "incomplete")
improving = ("improving", "not_improving")

#From searchlight 
soft_skills = (
    "Coachability", "Attention_to_Detail", "Hardworking", "Creativity",
    "Dependability", "Strategic Thinking", "Collaboration", "Trustworthiness",
    "Enthusiasm", "Persuasion", "Empathy", "Charisma", "Active Listening", "Humility",
    "Critical Thinking", "Adaptability", "Fast Learner", "Managing Stress",
    "Being a Self-Starter","Personable", "Curiosity", "Emotional Intelligence",
    "Poise", "Ambition", "Handling Ambiguity", "Competitiveness", "Methodical",
    "Customer-orientation", "Decisiveness", "Conscientiousness", "Teaching Others",
    "Independence", "Intelligence", "Intuition", "Good Judgement", "Optimism",
    "Persistence", "Problem Solving", "Results-driven", "Risk-taking", "Resourcefulness"   
                 )
mentee_other = (
    "communicating_with_other_mentors", "setting_expectations", "satisfied_with_progress"
)

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
    "Greyson", "Jordan", "Ian", "Carson", "Jaxson", "Leonardo", "Nicholas",
    "Dominic", "Austin", "Everett", "Brooks", "Xavier", "Kai", "Jose", "Parker",
    "Adam", "Jace", "Wesley", "Kayden", "Silas", "Bennett", "Declan", "Waylon",
    "Weston", "Evan", "Emmett", "Micah", "Ryder", "Beau", "Damian", "Brayden",
    "Gael", "Rowan", "Harrison", "Bryson", "Sawyer", "Amir", "Kingston",
    "Jason", "Giovanni", "Vincent", "Ayden", "Chase", "Myles", "Diego",
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
    "Hadley", "Arya", "Rose", "Reagan", "Eliza", "Adalynn", "Kaylee", "Lyla")

last_name = (
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
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez")
  


# + [markdown] id="L_eG2GjYLrpd"
# # Mock data classes
#

# + id="JGL_1jg5Luvw"
class Mentee:

    def __init__(self):
        self.profile_id = f"mentee{r.randint(1000000, 7000000000)}"
        self.first_name = r.choice(first_names)
        self.last_name = r.choice(last_name)
        self.skill_rank = r.sample(exp_level, k=1)
        self.industry = r.sample(industry, k=1)
        self.purpose = r.sample(purpose, k=r.randint(1, 3))
        self.roadblocks = r.sample(roadblocks, k=r.randint(1, 3))
        self.financial_aid = r.choice(financial_aid)
        self.showup = r.choice(showup)
        self.prepared = r.choice(prepared)
        self.homework = r.choice(homework)
        self.improving = r.choice(improving)

    @classmethod
    def to_df(cls, num_rows):
        return pd.DataFrame(vars(cls()) for _ in range(num_rows))


# + id="3SKJ3ib_JGr0"
class Mentor:

    def __init__(self):
        self.profile_id = f"mentor{r.randint(1000000, 7000000000)}"
        self.first_name = r.choice(first_names)
        self.last_name = r.choice(last_name)
        self.skill_rank = r.sample(exp_level, k=3)
        self.industry = r.sample(industry, k=1)
        self.purpose = r.sample(purpose, k=r.randint(1, 3))

    @classmethod
    def to_df(cls, num_rows):
        return pd.DataFrame(vars(cls()) for _ in range(num_rows))


# + [markdown] id="8KoL2_-00ir6"
# #Populating Mock Dataframes

# + id="K9X6IrRSRc76"
mentee = Mentee()
mentee_df = mentee.to_df(200)

# + id="-KrWTyj4KFbM"
mentor = Mentor()
mentor_df = mentor.to_df(50)

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="UdxAT2rWRwEH" outputId="e09458c7-44d9-4bc7-ff54-d644d0cfabf1"
mentor_df.head(5)

# + [markdown] id="9UcbF27T0tLh"
# # Improvements to be made

# + [markdown] id="P1g8PiTn0x78"
# To actually model the data and get results we need:
#   - Purpose to link to skills (maybe a drop down)
#   - Skills to link to skill rank 
#   - Skills and their rank to weigh in on purpose fulfillment
#   - Preliminary assumptions regarding 4 key metrics of show up prepared with homework done and improvements consistent. 
#     - The idea here being that the more often those metrics are met, the more successful the mentee will be... something only real data could reveal but assumptions being made are the way to mock that. 
#     - Plus, these could link to potential mentee attrition... how to avoid attrition through lack of attention/follow up/whatever. 
