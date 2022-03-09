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

# + id="joL2fzZzLV3I"
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="1q3tpf4wNC6v" outputId="07345553-c3b0-4325-cd27-3a0a3e61063a"
data1 = [['tom', 30, 1,1,0,0], ['nick', 35, 0,1,1,1], ['juli', 34, 1,1,0,1], ['Alex', 34, 1,0,0,0], ['Wei', 30, 0,0,1,1] ]
 

mentor = pd.DataFrame(data1, columns = ['Name', 'Age', 'Java', 'Python', 'CSS', 'JavaScript'])
 

mentor

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="ybyXddDySj10" outputId="cf042768-b0b3-4e94-b3b7-bbcb9475fb69"
data2 = [['A', 20, 1,0,0,1], ['B', 25, 0,0,1,0], ['C', 24, 0,1,0,1], ['D', 24, 0,0,1,0], ['E', 20, 1,0,1,0] ]
mentee = pd.DataFrame(data2, columns = ['Name', 'Age', 'Java', 'Python', 'CSS', 'JavaScript'])
 

mentee

# + colab={"base_uri": "https://localhost:8080/"} id="DETfnR-Md_Sq" outputId="f7887d2e-d8e6-4ac2-db79-3a15cdc7414e"
model = NearestNeighbors(n_neighbors=2, algorithm='brute')  # because we only have 5 mentors so I let the n_neighbor=2, but when we have more data, I think we can increase the n_neighbor based on the stakeholder willing
model.fit(mentor.drop(['Name','Age'],axis=1))

# + id="TM_jjdQtePDH"
n_dist, n_ind = model.kneighbors(mentee.drop(['Name','Age'],axis=1).head(1))
ind = list(n_ind[0])


# + [markdown] id="a1F23WQ3jMFd"
#

# + colab={"base_uri": "https://localhost:8080/"} id="yT3xXJo0e9xU" outputId="dcc873c8-a2ea-41c4-d703-98ceef83367a"

id_list = [1, 2]
mentor_list = []

for each in ind:
    mentor_list.append(mentor.iloc[each]["Name"])

recommendations = list(zip(id_list, mentor_list))

recommendations

# + [markdown] id="_nUbHagDjhi7"
# The 'recommendations' is list of mentors (Juli and Alex) matched for the first mentee.

# + id="v9wEBH1BfOju"

