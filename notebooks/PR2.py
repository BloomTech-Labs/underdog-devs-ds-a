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
# # This notebook is part#1, Vectorization, and part#2 PCA
#
# # Goal: modeling the possibility in end-result match of 1 mentee to multiple mentor candidates, or 1 mentor to multiple mentee candidates, or multiple mentor and mentee candidates in the same clustering. By vectorization and PCA preparation, for clustering of mentor and mentee in the similarity group of same interests, by considering gender, time zone, interest of life, and tech stack. One similarity group in one clustering of mentor and mentee; then the client can manually choose within the same clustering for the final match, as the client mentioned currently they would still prefer human intelligence for the final match with various reasons. The benefit of this model is one mentor may have bandwidth to coach multiple mentees, and one mentee may have several optional mentors for match-maker's decision; delivered by reading the same clustering the options provided for the match-maker.
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

# + colab={"base_uri": "https://localhost:8080/", "height": 337} id="eewKg9IMXApt" outputId="a37c72e9-7e20-4383-d334-11eadb018091"
raw_df.head()

# + [markdown] id="PBuEBFUL2ipZ"
# # Start preparing vectorization

# + id="leXa1oCgYDd1"
df = raw_df.drop(['ID', 'First Name', 'Last Name',
                                        'Gender', 'Time zone'],axis=1)

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="7F1JG-ujYNU6" outputId="715dbeea-008d-4b38-df3c-81a72f73fcf7"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 442} id="x83xzMyqesOo" outputId="6a190fb0-f17e-4cc0-ba58-6798bf5dbc32"
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
        


# + colab={"base_uri": "https://localhost:8080/"} id="MsfqUgDIexC5" outputId="bb13475d-696c-4681-d49f-e8a928addca6"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 462} id="UhLOEJuGYj-O" outputId="1387c155-bd4e-4ad4-9c5f-2da6a5991396"
# Creating a new DF that contains the vectorized words
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(df['Bios'])
df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
df_wrds

# + colab={"base_uri": "https://localhost:8080/", "height": 444} id="7wb8RYgRYonq" outputId="a5c64833-47e5-4b70-9309-529fdae8dba6"
# Concatenating the words DF with the original DF
new_df = pd.concat([df, df_wrds], axis=1)

# Dropping the Bios because it is no longer needed in place of vectorization
new_df.drop('Bios', axis=1, inplace=True)

# Viewing the new DF
new_df

# + colab={"base_uri": "https://localhost:8080/"} id="bvbS942gZJ2b" outputId="cd3f0f80-741e-438f-c5af-82362cf39d11"
new_df.shape

# + [markdown] id="-cjd3In5IWRV"
# end of vectorization

# + [markdown] id="nMWxvGUjIZ0E"
# #Part#2, PCA(Principal Component Analysis)
#
# #In order for us to reduce this large feature set, we implement PCA. This technique will reduce the dimensionality of our dataset but still retain much of the variability or valuable statistical information.

# + [markdown] id="krtaD0J6KWl3"
# # The following plot will visually tell us the number of features account for the variance.
#
# # X axis: # of Features accounting for % of the Variance
# # Y axis: Percent of variance
#

# + colab={"base_uri": "https://localhost:8080/", "height": 331} id="7Lx_kezmY16S" outputId="68df2b41-a812-48f9-dfaf-f08cd2e512e6"
from sklearn.decomposition import PCA

# Instantiating PCA
pca = PCA()

# Fitting and Transforming the DF
df_pca = pca.fit_transform(new_df)

# Plotting to determine how many features should the dataset be reduced to
plt.style.use("bmh")
plt.figure(figsize=(14,4))
print(pca.explained_variance_ratio_.cumsum()) 
plt.plot(np.cumsum((pca.explained_variance_ratio_)))
plt.show()
print(np.cumsum((pca.explained_variance_ratio_)))



# + [markdown] id="p4diVK2IDWQL"
# #After running our code, the number of features that account for 95% of the variance is 6. With that number in mind, we can apply it to our PCA function to reduce the number of Principal Components or Features in our last DF to 6 from 10.

# + [markdown] id="9cWAMbE8IMqr"
# #Finding the Right Number of Clusters
#
# # Below, we will be running some code that will run our clustering algorithm with differing amounts of clusters.

# + colab={"base_uri": "https://localhost:8080/", "height": 101, "referenced_widgets": ["8793375a99d14cc9af432b3fa11c8af7", "ccd1272eefbe4d7dadaecacceb02197f", "9151ca2c8fef47bfb86b08168cd11070", "8b90742791db4d5fbf66ddf6ddf298bc", "70ec13e7ffcf45df94955c9f42c6ef03", "99e0e5c72b564d5ca8d34c7f9c80da89", "61f22128c3c54aecb7cc08ed56e35550", "db9efefcb54c4a73bc3d491006936abe", "1f083d0ff35342ab8ccff94455f2a09d", "cd47032f36ca475bb1a0345181454881", "76024b0dc20e4d48944d6d27d53d8bd0"]} id="epfnL59kioOn" outputId="942a9390-294f-43f6-c43e-151df6752651"
from sklearn.metrics import calinski_harabasz_score, silhouette_score, davies_bouldin_score
# Setting the amount of clusters to test out
cluster_cnt = [i for i in range(2, 9, 1)]

# Establishing empty lists to store the scores for the evaluation metrics
ch_scores = []

s_scores = []

db_scores = []

# The DF for evaluation
eval_df = df_pca

# Looping through different iterations for the number of clusters
for i in tqdm(cluster_cnt):
    
    # Clustering with different number of clusters
    clust = AgglomerativeClustering(n_clusters=i, linkage='complete')
    
    clust.fit(eval_df)
    
    cluster_assignments = clust.labels_
    
    # Appending the scores to the empty lists
    ch_scores.append(calinski_harabasz_score(eval_df, cluster_assignments))
    
    s_scores.append(silhouette_score(eval_df, cluster_assignments))
    
    db_scores.append(davies_bouldin_score(eval_df, cluster_assignments))
