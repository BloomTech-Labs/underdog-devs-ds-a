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

# + colab={"base_uri": "https://localhost:8080/"} id="7FRteWcPKJ_N" outputId="101d4c16-f501-44eb-ef5f-9b7f156e5e46"
# !pip install Fortuna

# + [markdown] id="hDeER8SnLOJD"
# - Track 70/30 or 80/20
# - Age 18-60
# - Gender 80/18/2

# + colab={"base_uri": "https://localhost:8080/"} id="Nhp4j2geMqsN" outputId="5c53e04f-75b0-40e4-ea80-264ebd158272"
# !pip install MonkeyScope

# + [markdown] id="LZ589M52__My"
# - Importing Fortuna library

# + id="z3Ttx4LfMCO4"
from Fortuna import random_int,percent_true,RandomValue

# + colab={"base_uri": "https://localhost:8080/"} id="z1K5uHkeMHCu" outputId="328186e7-f7d7-4314-cdb8-0e19493d41f9"
random_int(1,20)

# + id="lCfQ7_JkMRY7"
random_track = lambda : "Web" if percent_true(80) else "DS"

# + colab={"base_uri": "https://localhost:8080/", "height": 35} id="pQ9iir5DMfZ0" outputId="905ac1bc-66b0-44e7-dbc0-9f0b27309e1c"
random_track()

# + [markdown] id="0p0h_KHX_4aP"
# - Importing MonkeyScope Library

# + id="C6_PpyTGM3jH"
from MonkeyScope import distribution

# + colab={"base_uri": "https://localhost:8080/"} id="3RRJPObLM8Q8" outputId="3cff92cf-f749-4897-9208-f8b7e5e684e1"
distribution(random_track)

# + id="dRVk9kJDNDc1"
random_gender = lambda : "Male" if percent_true(80) else "Female" if percent_true(90) else "Non-Binary"

# + colab={"base_uri": "https://localhost:8080/"} id="24wbOix_NT82" outputId="0755e3e7-317b-401b-fdd4-207f5ccd0566"
distribution(random_gender)

# + [markdown] id="y-P14DzD9zda"
# - Poisson Distribution is a Discrete Distribution. It estimates how many times an event can happen in a specified time

# + id="OdVZrTj_NZ_S"
from Fortuna import front_poisson

# + colab={"base_uri": "https://localhost:8080/"} id="DhKFxgZMN1vV" outputId="e8f3415f-8a05-4380-e14d-0e1a8c4bfdb6"
distribution(front_poisson,20)

# + id="R4Ei9u_kOGGt"
random_age = RandomValue(range(18,61),front_poisson)

# + colab={"base_uri": "https://localhost:8080/"} id="F-R7ObUiRUzI" outputId="09bec394-a6ee-43e9-eba8-791bc77ffd39"
random_age()

# + colab={"base_uri": "https://localhost:8080/"} id="Kz4QDAJFRYAF" outputId="ae595e24-be37-48bc-aeec-3b68243cc9d0"
distribution(random_age)

# + [markdown] id="SYePCtH7_Cbx"
# - CumulativeWeightedChoice takes a set of numbers representing the weight that are Cumulative in nature.
# - RelativeWeightedChoice takes a set of numbers representing the weight that are Relative in nature

# + id="Qi9QFibBSAnP"
from Fortuna import CumulativeWeightedChoice, RelativeWeightedChoice


# + id="V0LpfSGORtXP"
class RandomUser:
    random_age = RandomValue(
        range(18,60),
        front_poisson,
    )
    random_track = CumulativeWeightedChoice((
        (80, "Web"),
        (100, "DS"),
    ))
    random_gender = RelativeWeightedChoice((
        (80, "Male"),
        (18, "Female"),
        (2, "Non-binary"),      
    ))

    def __init__(self):
        self.age = self.random_age()
        self.track = self.random_track()
        self.gender = self.random_gender()

    def __repr__(self):
        output = (
            f"Track : {self.track}",
            f"Age : {self.age}",
            f"Gender : {self.gender}",
        )
        return "\n" .join(output)

    def to_dict(self):
        return {
            "Track" : self.track,
            "Age" : self.age,
            "Gender" : self.gender
            
        }



# + colab={"base_uri": "https://localhost:8080/"} id="DSLaTvCLUsYF" outputId="e0e804a4-967f-425c-a1f5-3c540a3b9ab7"
user = RandomUser()
user

# + id="mi97flGAU4CJ"
import pandas as pd


# + id="NqOn9vOfU7zS"
df = pd.DataFrame(RandomUser().to_dict() for _ in range(1000000))

# + [markdown] id="gC6lEWsnDVYl"
# - Generated Data frame with 1 million rows and 3 columns Track,Age and Gender

# + colab={"base_uri": "https://localhost:8080/", "height": 423} id="sCrImZopVF3R" outputId="0ba758bb-96f5-401e-afe6-39f175276f3b"
df
