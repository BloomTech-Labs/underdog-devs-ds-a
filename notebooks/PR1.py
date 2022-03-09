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

# + [markdown] id="07nznDwVtoCb"
#
#
# # Mentor-Mentee Match, via Vectorization, PCA(Principal Component Analysis), Clustering, and Test Search for the Best Model
#
# # This notebook is part#1, Vectorization
#
# # Goal: modeling the possibility in end-result match of 1 mentee to multiple mentor candidates, or 1 mentor to multiple mentee candidates, or multiple mentor and mentee candidates in the same clustering. By vectorization and PCA preparation, for clustering of mentor and mentee in the similarity group of same interests, by considering gender, time zone, interest of life, and tech stack. One similarity group in one clustering of mentor and mentee; then the client can manually choose within the same clustering for the final match, as the client mentioned currently they would still prefer human intelligence for the final match with various reasons. The benefit of this model is one mentor may have bandwidth to coach multiple mentees, and one mentee may have several optional mentors for match-maker's decision; delivered by reading the same clustering the options provided for the match-maker.
#
#

# + id="okvAtRRCWs_z"
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import AgglomerativeClustering
#from sklearn.metrics import calinski_harabaz_score, silhouette_score, davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from tqdm import tqdm_notebook as tqdm

# + id="1pwEahu6XK-Q"
# mock-up dataset in csv file with 10 observations
# we could also take the excel file from client converted to csv for modeling experiments

raw_df  = pd.read_csv('Mentor_Mentee.csv')

# + [markdown] id="0epfRDkv0tFB"
# # The dataset (could be an excel file from client) consists of personal info, tech stack(For mentee, it is the interest level to learn on scale of 1 to 10. For mentor, it is the proficiency level on scale of 1 to 10.) Bios, could be a check-box type survey or each person's own words; and list of different interests of life on scale of 1 to 10.

# + colab={"base_uri": "https://localhost:8080/", "height": 337} id="eewKg9IMXApt" outputId="c5e28c4b-63ed-44bd-8dd0-04cdcf0922f1"
raw_df.head()

# + [markdown] id="PBuEBFUL2ipZ"
# # Start preparing vectorization

# + id="leXa1oCgYDd1"
df = raw_df.drop(['ID', 'First Name', 'Last Name',
                                        'Gender', 'Time zone'],axis=1)

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="7F1JG-ujYNU6" outputId="e704b12f-5a47-4148-fd23-fc19276de02f"
df.head()


# + id="wge_dF7CYieG"
def string_convert(x):
    """
    First converts the lists in the DF into strings
    """
    if isinstance(x, list):
        return ' '.join(x)
    else:
        return x
    
# Looping through the columns and applying the function
for col in df.columns:
    df[col] = df[col].apply(string_convert)

# + colab={"base_uri": "https://localhost:8080/", "height": 442} id="x83xzMyqesOo" outputId="02acf522-0acd-431a-a526-71fac59d1aa0"
df


# + [markdown] id="ld90LgpFwmBC"
# # Vectorization

# + id="iHEkAYiSevFu"
def vectorization(df, columns):
    """
    Using recursion, iterate through the df until all the categories have been vectorized
    """
    column_name = columns[0]
    
    # Checking if the column name has been removed already
    if column_name not in ['Bios', 'Movies','Religion', 'Music', 'Books', 'Sports']:
        return df
    
    if column_name in ['Religion']:
        df[column_name.lower()] = df[column_name].cat.codes
        
        df = df.drop(column_name, 1)
        
        return vectorization(df, df.columns)
    
    else:
        # Instantiating the Vectorizer
        vectorizer = CountVectorizer()
        
        # Fitting the vectorizer to the Bios
        x = vectorizer.fit_transform(df[column_name])

        # Creating a new DF that contains the vectorized words
        df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())

        # Concating the words DF with the original DF
        new_df = pd.concat([df, df_wrds], axis=1)

        # Dropping the column because it is no longer needed in place of vectorization
        new_df = new_df.drop(column_name, axis=1)
        
        return vectorization(new_df, new_df.columns) 


# + colab={"base_uri": "https://localhost:8080/"} id="MsfqUgDIexC5" outputId="e5cc3be3-d629-46a0-b514-b651bc3b6c09"
# Creating the vectorized DF
vect_df = vectorization(df, df.columns)

# + [markdown] id="cNi0bsjxwwdh"
# # Scaling the data
#
# # It will assist our clustering algorithm’s performance, is scaling categories. This will potentially decrease the time it takes to fit and transform our clustering algorithm to the dataset.
#

# + id="6tocrbLkh4bQ"
scaler = MinMaxScaler()
# vect_df  = pd.DataFrame(scaler.fit_transform(new_df), 
#                                columns=new_df.columns,
#                                index=new_df.index)


vect_df = pd.DataFrame(scaler.fit_transform(vect_df), index=vect_df.index, columns=vect_df.columns)

#pd.DataFrame(scaler.fit_transform(vect_df), index=vect_df.index, columns=vect_df.columns)

# + colab={"base_uri": "https://localhost:8080/", "height": 462} id="UhLOEJuGYj-O" outputId="2970e953-b2b4-4848-d096-d10a5d5678e7"
# Creating a new DF that contains the vectorized words
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(df['Bios'])
df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
df_wrds

# + colab={"base_uri": "https://localhost:8080/", "height": 444} id="7wb8RYgRYonq" outputId="c0de80d0-db4e-4f08-a466-bbceda83289b"
# Concatenating the words DF with the original DF
new_df = pd.concat([df, df_wrds], axis=1)

# Dropping the Bios because it is no longer needed in place of vectorization
new_df.drop('Bios', axis=1, inplace=True)

# Viewing the new DF
new_df

# + colab={"base_uri": "https://localhost:8080/"} id="bvbS942gZJ2b" outputId="09384ba2-bf2e-4205-c014-cf75cfb81890"
new_df.shape
