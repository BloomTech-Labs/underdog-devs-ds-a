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

# + [markdown] id="SjVMCQCmYqhr"
# ## Example Notebook

# + id="OCmK5JPfYb8L"
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# + [markdown] id="-M8WwVztY8rB"
# ### Mentor Data

# + colab={"base_uri": "https://localhost:8080/", "height": 143} id="Gkr7ZbXWY5d_" outputId="f8b29515-d2fb-4ab1-97a8-c2e1ad86dd20"
mentor_data = pd.DataFrame([
    {
        "Name": "Tom",
        "Python": 1,
        "HTML": 0,
        "CSS": 0,
        "JavaScript": 0,
    },
    {
        "Name": "Nick",
        "Python": 0,
        "HTML": 1,
        "CSS": 1,
        "JavaScript": 1,
    },
    {
        "Name": "Juli",
        "Python": 1,
        "HTML": 1,
        "CSS": 1,
        "JavaScript": 1,
    },
])
mentor_data

# + [markdown] id="JLwz-GWnZTEa"
# ### Mentee Data

# + colab={"base_uri": "https://localhost:8080/", "height": 143} id="iCSuBJsGZNCF" outputId="82d0736b-4e8c-4f6d-e1a5-ad0a933defcf"
mentee_data = pd.DataFrame([
    {
        "Name": "Adam",
        "Python": 0,
        "HTML": 1,
        "CSS": 1,
        "JavaScript": 1,
    },
    {
        "Name": "Brad",
        "Python": 1,
        "HTML": 0,
        "CSS": 0,
        "JavaScript": 0,
    },
    {
        "Name": "Lucy",
        "Python": 1,
        "HTML": 1,
        "CSS": 1,
        "JavaScript": 1,
    },
])
mentee_data

# + [markdown] id="sX4_ZH2vZz81"
# ## Nearest Neighbors Model

# + colab={"base_uri": "https://localhost:8080/"} id="QirBpivUZgGo" outputId="4b9bd51e-746b-4982-e43d-b5eb12ee3f7f"
model = NearestNeighbors(n_neighbors=1, algorithm="brute")
model.fit(mentor_data.drop(columns=["Name"]))

# + [markdown] id="bm0vo15SZ4MQ"
# ### Find Matches

# + colab={"base_uri": "https://localhost:8080/", "height": 143} id="kBj--7_kZrjf" outputId="f8e8c848-19c5-407e-fea0-2c1c4ded8ed5"
matches = model.kneighbors(mentee_data.drop(columns=["Name"]), return_distance=False)
matches_data = pd.DataFrame(matches, columns=["Mentor"])
matches_data.index.names = ["Mentee"]
matches_data = matches_data.reset_index()
matches_data


# + id="Zw7i4Qpjabri"
def mentor_lookup(idx):
    return mentor_data.iloc[idx]["Name"]


# + id="bdKZ0Vihatkh"
def mentee_lookup(idx):
    return mentee_data.iloc[idx]["Name"]


# + id="g5r6nThRbfQ2"
from pandas import DataFrame


# + id="KTJDbf7Sau2c"
def lookup(idx: int, data: DataFrame):
    return data.iloc[idx]["Name"]


# + colab={"base_uri": "https://localhost:8080/", "height": 143} id="N8e-E9fwbdhl" outputId="5b329884-5dcf-436d-f756-113e9add5f7d"
matches_data["Mentee"] = matches_data["Mentee"].apply(mentee_lookup)
matches_data["Mentor"] = matches_data["Mentor"].apply(mentor_lookup)
matches_data

# + id="JSXxwNrycEGm"

