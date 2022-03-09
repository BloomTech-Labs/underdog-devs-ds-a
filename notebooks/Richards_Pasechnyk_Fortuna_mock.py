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

# + [markdown] id="3U8wUpqgESep"
# #Install Libraries

# + colab={"base_uri": "https://localhost:8080/"} id="2UpMLwiqSZIa" outputId="18417bac-8794-4dfc-ebde-cb18b2d7e14e"
# !pip install Fortuna #randomness
# !pip install names
# !pip install MonkeyScope

# + [markdown] id="LiyjUrmTEbkJ"
# #Import Libraries

# + id="_gpnhVdXJ_9q"
import pandas as pd
from Fortuna import random_int, percent_true, FlexCat, RelativeWeightedChoice
from MonkeyScope import distribution

# + [markdown] id="xlJwcAi0RCnO"
# #Mock Dictionary To Take Items From

# + id="7ijnzNKI9d86"
# Took names from other notebooks, thanks January/February cohort

mock_dict = {
    "male_first_names": (
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
    "Nathaniel", "Legend", "Jonah", "River", "Tyler", "Cole", "Braxton",
    "George", "Milo", "Zachary", "Ashton", "Luis", "Jasper", "Kaiden", "Adriel",
    "Gavin", "Bentley", "Calvin", "Zion", "Juan", "Maxwell", "Max", "Ryker",
    "Carlos", "Emmanuel", "Jayce", "Lorenzo", "Ivan", "Jude", "August", "Kevin",
    "Malachi", "Elliott", "Rhett", "Archer", "Karter", "Arthur", "Luka",
    "Elliot", "Thiago", "Brandon", "Camden", "Justin", "Jesus", "Maddox",
    "King", "Theo", "Enzo", "Matteo", "Emiliano", "Dean", "Hayden", "Finn",
    "Brody", "Antonio", "Abel", "Alex", "Tristan", "Graham", "Zayden", "Judah",
    "Xander", "Miguel", "Atlas", "Messiah", "Barrett", "Tucker", "Timothy",
    "Alan", "Edward", "Leon", "Dawson", "Eric", "Ace", "Victor", "Abraham",
    "Nicolas", "Jesse", "Charlie", "Patrick", "Walker", "Joel", "Richard",
    "Beckett", "Blake", "Alejandro", "Avery", "Grant", "Peter", "Oscar",
    "Matias", "Amari", "Lukas", "Andres", "Arlo", "Colt", "Adonis", "Kyrie",
    "Steven", "Felix", "Preston", "Marcus", "Holden", "Emilio", "Remington",
    "Jeremy", "Kaleb", "Brantley", "Bryce", "Mark", "Knox", "Israel", "Phoenix",
    "Kobe", "Nash", "Griffin", "Caden", "Kenneth", "Kyler", "Hayes", "Jax",
    "Rafael", "Beckham", "Javier", "Maximus", "Simon", "Paul", "Omar", "Kaden",
    "Kash", "Lane", "Bryan", "Riley", "Zane", "Louis", "Aidan", "Paxton",
    "Maximiliano", "Karson", "Cash", "Cayden", "Emerson", "Tobias", "Ronan",
    "Brian", "Dallas", "Bradley", "Jorge", "Walter", "Josue", "Khalil",
    "Damien", "Jett", "Kairo", "Zander", "Andre", "Cohen", "Crew", "Hendrix",
    "Colin", "Chance", "Malakai", "Clayton", "Daxton", "Malcolm", "Lennox",
    "Martin", "Jaden", "Kayson", "Bodhi", "Francisco", "Cody", "Erick",
    "Kameron", "Atticus", "Dante", "Jensen", "Cruz", "Finley", "Brady" 
    ),

    "female_first_names": (
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
    "Genevieve", "Alina", "Bailey", "Juniper", "Maeve", "Molly", "Harmony",
    "Georgia", "Magnolia", "Catalina", "Freya", "Juliette", "Sloane", "June",
    "Sara", "Ada", "Kimberly", "River", "Ember", "Juliana", "Aliyah", "Millie",
    "Brynlee", "Teagan", "Morgan", "Jordyn", "London", "Alaina", "Olive",
    "Rosalie", "Alyssa", "Ariel", "Finley", "Arabella", "Journee", "Hope",
    "Leila", "Alana", "Gemma", "Vanessa", "Gracie", "Noelle", "Marley", "Elise",
    "Presley", "Kamila", "Zara", "Amy", "Kayla", "Payton", "Blake", "Ruth",
    "Alani", "Annabelle", "Sage", "Aspen", "Laila", "Lila", "Rachel", "Trinity",
    "Daniela", "Alexa", "Lilly", "Lauren", "Elsie", "Margot", "Adelyn", "Zuri",
    "Brooke", "Sawyer", "Lilah", "Lola", "Selena", "Mya", "Sydney", "Diana",
    "Ana", "Vera", "Alayna", "Nyla", "Elaina", "Rebecca", "Angela", "Kali",
    "Alivia", "Raegan", "Rowan", "Phoebe", "Camilla", "Joanna", "Malia"),
    
    "last_names": (
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
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"),
         
    "city": (
    "Nova", "Amali", "Fernanda", "Alia", "Angeli", "Elliot", "Justice",
    "Maeyor", "Ceceli", "Glori", "Ariya", "Virginia", "Cheyenne", "Aleah",
    "Jemma", "Henley", "Meredith", "Leyla", "Lennox", "Ensley", "Zahra",
    "Reina", "Frankie", "Lylah", "Nalani", "Reyna", "Saige", "Ivanna", "Aleena",
    "Emerie", "Ivory", "Leslie", "Alora", "Ashlyn", "Bethany", "Bonnie",
    "Sasha", "Xiomara", "Salem", "Adrianna", "Dayana", "Clementine", "Karina",
    "Karsyn", "Emmie", "Julie", "Julieta", "Briana", "Carly", "Macy", "Marie",
    "Oaklee", "Christina", "Malaysia", "Ellis", "Irene", "Anne", "Anahi",
    "Mara", "Rhea", "Davina", "Dallas", "Jayda", "Mariam", "Skyla", "Siena",
    "Elora", "Marilyn", "Jazmin", "Megan", "Rosa", "Savanna", "Allyson",
    "Milan", "Coraline", "Johanna", "Melany", "Chelsea", "Michaela", "Melina",
    ),

    "append": (
      "st.", "pl.", "rd.", "ln.", "ave.", "blvd.", "ct.", "plaza", "terrace",
      "run", "trail"),

    "state": (
    "Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", 
    "Colorado", "Connecticut", "D.C.", "Delaware", "Florida", 
    "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", 
    "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine",  
    "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", 
    "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", 
    "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
    "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", 
    "Washington", "Wisconsin", "West Virginia", "Wyoming", "Michigan"   
    ),
    
    "industry":
     ("unsure", "health and wellness", "data storage and security", "customer relationship management", "travel", "accounting and finance",
     "application and data integration", "human resources and workforce management", "supply chain and logistics", "food and grocery",
     "web development", "lighting and LED", "infrastructure and hosting", "collaboration and project management", "data and broadband",
     "music", "real estate"),

    "time_of_day": 
    ("Morning: 6am-10am",
    "noon: 10am-2pm",
    "afternoon: 2pm-6pm",
    "Evening: 6pm-9pm"),
    }

# + id="u_OOEH7kVHFj"
gend = {"gender":
    ("female", "male", "transgender", "non-binary/non-conforming",  "prefer not to say"),
}

lang = {"language_preference":
    ("english", "spanish", "chinese", "other")
}

exp = {"experience":
     ("none", "beginner", "intermediate", "advanced"), 
}

tech = {"tech_stack":
     ("JavaScript", "HTML", "CSS", "Python", "SQL", "React", "Redux", "Java", "Node.js", "Typescript",
      "C#", "Bash/Shell", "C++", "PHP", "C", "Powershell", "Go", "Kotlin", "Rust", "Ruby",
      "Dart", "Assembly", "Swift", "R", "Redux"), "new_stack": "unsure"
}

#From searchlight 
soft_skills = { "career" :
    ("Coachability", "Attention_to_Detail", "Hardworking", "Creativity",
    "Dependability", "Strategic Thinking", "Collaboration", "Trustworthiness",
    "Enthusiasm", "Persuasion", "Empathy", "Charisma", "Active Listening", "Humility",
    "Critical Thinking", "Adaptability", "Fast Learner", "Managing Stress",
    "Being a Self-Starter","Personable", "Curiosity", "Emotional Intelligence",
    "Poise", "Ambition", "Handling Ambiguity", "Competitiveness", "Methodical",
    "Customer-orientation", "Decisiveness", "Conscientiousness", "Teaching Others",
    "Independence", "Intelligence", "Intuition", "Good Judgement", "Optimism",
    "Persistence", "Problem Solving", "Results-driven", "Risk-taking", "Resourcefulness")   
}

ind = {"industry":
     ("unsure", "health and wellness", "data storage and security", "customer relationship management", "travel", "accounting and finance",
     "application and data integration", "human resources and workforce management", "supply chain and logistics", "food and grocery",
      "web development", "lighting and LED", "infrastructure and hosting", "collaboration and project management", "data and broadband",
       "music", "real estate"),
}
tizo = {"time_zone":
      ("EST(New York)", "CST(Chicago)", "MST(Denver)", "PST(Los Angeles)",
  "GMT(London)", "AST(Saudi Arabia)", "JST(Japan)"), 
}
tod = {"time_of_day": 
  ("Morning: 6am-10am",
  "noon: 10am-2pm",
  "afternoon: 2pm-6pm",
  "Evening: 6pm-9pm"),
}
#some disclaimer here: your application will not be denied on the basis of stating that you are not comfortable sharing
conv = {"convictions":
    ("not comfortable sharing", "misdemeanor", "felony", "none"),
}
#some disclaimer here: your application will not be denied on the basis of stating that you are not comfortable sharing
toc = {"type_of_crime":
    ("not comfortable sharing","crime against a person", "crime against property", "inchoate", "statutory", "financial", "cyber", "other"),
     "other":("N/A", "not comfrotable sharing")
}

#Are underdog devs adverstizing? Will they be? This should populate with where they are investing in marketing
refer = {"referred":
    ("friend", "mentor", "google", "facebook", "linkedin"),
}

# + [markdown] id="X6XrnqlumDtC"
# #Combined Application Features
#  - Personal Information\
#     - Profile ID\
#     - First Name \ Last Name \
#     - Email \ Phone Number \
#     - Gender \
#     - Date of birth \
#     - Street Address \ zipcode \ city \ state \
#     - Time Zone \
#     - Veteran Status \
#     - Multilingual? Language preference \
#     - Convictions \ type of crime \
#     - financial assistance needed \ material resources needed
# (more stringent checkins and address may be needed if this is a yes) \
#
# - Career Information
#     - Tech/Career/Life/All \
#     - Tech Stack \
#     - Years of Experience per stack \
#     - Industry \
#     - Hobbies \ Interests \
#     - Number of Mentees \
#     - Time of day \
#
# - Other:
#     - how did you hear about us? \
#     - anything you want us to know \
#     - date_submitted 

# + [markdown] id="n_mfSwRXfBLk"
# #Functions to call in classes

# + [markdown] id="LhL8nt05VwZq"
# ### Accurately gendered names

# + id="rB9iTBaq9dgA"
# FlexCat works with the dictionary to choose called random values from the keys
random_name = FlexCat(mock_dict, key_bias = "flat_uniform")


# + id="EeD3ZckXquuX"
def gender():
  if percent_true(75):
    return "male"
  if percent_true(85):
    return "female"
  if percent_true(20):
    return "transgender"
  if percent_true(75):
    return "non_binary"
  else:
    return "prefer_not_to_say"


# + id="_W8fnnJ1q99A"
def firstname():
  if gender() == "male":
    return random_name("male_first_names")
  if gender() == "female":
    return random_name("female_first_names")
  else:
    return random_name("male_first_names", "female_first_names", "last_names")


# + [markdown] id="BpEaExSsIdRr"
# ## Weights and languages from Statista_Data Notebook from Dan Kositzke
#

# + id="qJrXE0Fmu1EJ"
mentor_stack = ["JavaScript", "HTML", "CSS", "Python", "SQL", "React", "Redux", "Java", "Node.js", "Typescript",
      "C#", "Bash/Shell", "C++", "PHP", "C", "Powershell", "Go", "Kotlin", "Rust", "Ruby",
      "Dart", "Assembly", "Swift", "R", "Redux"]

# + id="LlCJncRTHvYg"
#Notice that "unsure" is in this list vs. the mentor list. 
mentee_stack = ["JavaScript", "HTML", "CSS", "Python", "SQL", "Unsure", "React", "Redux", "Java", "Node.js", "Typescript",
      "C#", "Bash/Shell", "C++", "PHP", "C", "Powershell", "Go", "Redux", "Rust", "Ruby",
      "Dart", "Assembly", "Swift", "R"]


# + id="zyZ6wY0N_8WT"
weights = [64.96, 56.07, 48.24, 47.08, 35.35, 33.91, 30.19, 27.86,
27.13, 24.31, 21.98, 21.01, 10.75, 9.55, 8.32, 7.03, 6.75, 6.02, 5.61, 5.1,
5.07, 4.66, 4.66, 3.01, 2.8]

# + id="4o6hb3QjFEVb"
mentor_weighted = RelativeWeightedChoice(zip(weights, mentor_stack))

# + id="d-7TYILUIHBk"
mentee_weighted = RelativeWeightedChoice(zip(weights, mentee_stack))


# + [markdown] id="ggq1McQOV5fs"
# ### statistically accurate weighted techstacks 

# + id="P-sI6HXA_8ik"

def techStack():
    techstack = []
    for i in range(5):
        techstack += [mentor_weighted()]
    return techstack


# + colab={"base_uri": "https://localhost:8080/"} id="uam-Zkm6OubP" outputId="860d1daf-d1a2-438d-904d-72ef3c12d431"
techStack()


# + id="w1mfam-0_88S"
def newStack():
    newstack = []
    for i in range(5):
        newstack += [mentee_weighted()]
    return newstack


# + [markdown] id="caaSKApKDBdZ"
# ### Simple Functions

# + id="GhrUXnhj_9HN"
timezone = FlexCat(tizo, key_bias= "front_linear", val_bias = "front_poisson")

# + id="EzdgWPKw-SCS"
language_preference = FlexCat(lang, key_bias = "front_linear", val_bias = "front_gauss")

# + id="CSjI30rl-ohf"
financialaid = percent_true(50.0)

# + [markdown] id="mUAoMsQfNiKB"
# ### Convitions and type of crime related

# + colab={"base_uri": "https://localhost:8080/", "height": 35} id="fQvZ2vbphSQV" outputId="a5a8bded-6ff6-4114-d40f-bf028249bd60"
convictions = FlexCat(conv, val_bias = "flat_uniform")
typecrime = FlexCat(toc, val_bias= "flat_uniform")
typecrime(cat_key="other")


# + id="ywdzkfghJHMF"
def type_of_crime():
    if convictions() == "none" or convictions() == "not comfortable sharing":
      return "N/A"
    else:
      return typecrime(cat_key="type_of_crime")


# + [markdown] id="XJWsfUZKn1Z6"
# #Classes 

# + id="hITvjHLevchs"
class Mentee:

    
    def __init__(self):
        self.profile_id = f"mentee{random_int(1111111,999999999)}"
        self.first_name = firstname()
        self.last_name = random_name("last_names")
        self.email = f"{self.first_name}_{self.last_name}{random_int(1,1000)}@fake.com"
        self.phone_number = f"({random_int(100, 999)})-{random_int(100, 999)}-{random_int(1000, 9999)}"
        self.gender = gender()
        self.timezone = timezone()
        self.street_address = f"{random_int(11,99999)} {random_name('last_names')} {random_name('append')}"
        self.city = random_name("city")
        self.state = random_name("state")
        self.veteran_status = percent_true(10.0)
        self.language_preference = language_preference()
        self.convictions = convictions()
        self.crimes = type_of_crime()
        self.financialaid = percent_true(50.0)
        self.new_stack = newStack()



    def __repr__(self):
        output = (
            f"Profile ID: {self.profile_id}",
            f"First Name: {self.first_name}",
            f"Last Name: {self.last_name}",
            f"Gender: {self.gender}",
            f"Language Preference: {self.language_preference}",
            f"Veteran: {self.veteran_status}",
            f"Email: {self.email}",
            f"Phone Number: {self.phone_number}",
            f"Street Address: {self.street_address}",
            f"City: {self.city}",
            f"State: {self.state}",
            f"Time Zone: {self.timezone}",
            f"Conviction: {self.convictions}",
            f"Type of crime: {self.crimes}",
            f"Financial Aid: {self.financialaid}",
            f"Tech Stack: {self.new_stack}",
        )
        return "\n".join(output)
    
    def to_dict(self):
        return {
            "Profile ID": self.profile_id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Gender": self.gender,
            "Language Preference": self.language_preference,
            "Veteran": self.veteran_status,
            "Email": self.email,
            "Phone Number": self.phone_number,
            "Street Address": self.street_address,
            "City": self.city,
            "State": self.state,
            "Time Zone": self.timezone,
            "Conviction": self.convictions,
            "Type of crime": self.crimes,
            "Financial Aid": self.financialaid,
            "Tech Stack": self.new_stack,
        }


# + id="uKvk1t0CarpD"
class Mentor:

    
    def __init__(self):
        self.profile_id = f"mentor{random_int(1111111,999999999)}"
        self.first_name = firstname()
        self.last_name = random_name("last_names")
        self.email = f"{self.first_name}_{self.last_name}{random_int(1,1000)}@fake.com"
        self.phone_number = f"({random_int(100, 999)})-{random_int(100, 999)}-{random_int(1000, 9999)}"
        self.gender = gender()
        self.street_address = f"{random_int(11,99999)} {random_name('last_names')} {random_name('append')}"
        self.city = random_name("city")
        self.state = random_name("state")
        self.timezone = timezone()
        self.veteran_status = percent_true(10.0)
        self.language_preference = language_preference()
        self.tech_stack = techStack()



    def __repr__(self):
        output = (
            f"Profile ID: {self.profile_id}",
            f"First Name: {self.first_name}",
            f"Last Name: {self.last_name}",
            f"Gender: {self.gender}",
            f"Language Preference: {self.language_preference}",
            f"Veteran: {self.veteran_status}",
            f"Email: {self.email}",
            f"Phone Number: {self.phone_number}",
            f"Street Address: {self.street_address}",
            f"City: {self.city}",
            f"State: {self.state}",
            f"Time Zone: {self.timezone}",
            f"Tech Stack: {self.tech_stack}",

            

        )
        return "\n".join(output)
    
    def to_dict(self):
        return {
            "Profile ID": self.profile_id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Gender": self.gender,
            "Language Preference": self.language_preference,
            "Veteran": self.veteran_status,
            "Email": self.email,
            "Phone Number": self.phone_number,
            "Street Address": self.street_address,
            "City": self.city,
            "State": self.state,
            "Time Zone": self.timezone,
            "Tech Stack": self.tech_stack,
        }


# + id="cRXC9K109dXq"
mentee = Mentee()

# + colab={"base_uri": "https://localhost:8080/"} id="e6Fw4bHxc4iS" outputId="067a1d81-783c-47a1-fd86-e678320660c6"
mentee

# + id="eOpDI08PSqDc"
mentor = Mentor()

# + colab={"base_uri": "https://localhost:8080/"} id="MFR1pP1xBvow" outputId="aec88378-fb24-4a9d-908e-716286b039e7"
mentor

# + [markdown] id="iS1Hdv8VRlbH"
# # Populate a dataframe with mock data
#
#

# + id="EVq_4s-2cRUq"
mentee_df = pd.DataFrame(Mentee().to_dict() for i in range(1000))

# + colab={"base_uri": "https://localhost:8080/", "height": 617} id="89QZ_PWNdIVg" outputId="9e9e69e7-4460-431d-c43e-ed83227f04ba"
mentee_df.head()

# + id="iGvI5VfZCDEi"
mentor_df = pd.DataFrame(Mentor().to_dict() for i in range(1000))

# + colab={"base_uri": "https://localhost:8080/", "height": 441} id="Y14RxDmMCHHE" outputId="16567599-7216-40d7-c8b3-6c46bce2e476"
mentor_df.head(5)
