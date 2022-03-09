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
#
# # Mentor-Mentee Match, via Vectorization, PCA(Principal Component Analysis), Clustering, and Test Search for the Best Model
#
# # This notebook is part#1, Vectorization, part#2 PCA, and part#3 Clustering
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

# + colab={"base_uri": "https://localhost:8080/", "height": 337} id="eewKg9IMXApt" outputId="3c445749-dfee-44dd-ffb0-da249b9f4d72"
raw_df.head()

# + [markdown] id="PBuEBFUL2ipZ"
# # Start preparing vectorization

# + id="leXa1oCgYDd1"
df = raw_df.drop(['ID', 'First Name', 'Last Name',
                                        'Gender', 'Time zone'],axis=1)

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="7F1JG-ujYNU6" outputId="5068f699-dfdf-4263-a997-9ff6fea3b6f6"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 442} id="x83xzMyqesOo" outputId="c068d9ca-b407-46d5-b62c-7127eba64f72"
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
        


# + colab={"base_uri": "https://localhost:8080/"} id="MsfqUgDIexC5" outputId="18f8a1b4-aa62-4f24-a510-5655a94673f6"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 462} id="UhLOEJuGYj-O" outputId="a057627c-afb9-4b19-fb4a-02cdbb86be3a"
# Creating a new DF that contains the vectorized words
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(df['Bios'])
df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
df_wrds

# + colab={"base_uri": "https://localhost:8080/", "height": 444} id="7wb8RYgRYonq" outputId="cc884b4f-e81e-4acb-c492-c363d9566039"
# Concatenating the words DF with the original DF
new_df = pd.concat([df, df_wrds], axis=1)

# Dropping the Bios because it is no longer needed in place of vectorization
new_df.drop('Bios', axis=1, inplace=True)

# Viewing the new DF
new_df

# + colab={"base_uri": "https://localhost:8080/"} id="bvbS942gZJ2b" outputId="6913ff53-0f1c-4034-8f1d-b1ca34350d41"
new_df.shape

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

# + colab={"base_uri": "https://localhost:8080/", "height": 331} id="7Lx_kezmY16S" outputId="09080bdc-d0d5-47be-9584-602db3fde7c1"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 101, "referenced_widgets": ["eea594f1da924ef7ae57a3099920a656", "de308e5ee7404e068ecc3aed1b83d522", "ce3dcc7c63624b8cacb699f45515e407", "6902b860ae8a40dfb14d99ef669864c3", "f9dfb64b6b6d4fb5853fb25886448a34", "217582d7333a4669b4fd2d888e8bd569", "075a617d62cf4ab491285db9bd484f53", "28f68017cc5241488c44b0a46678c261", "35e1e73d36f84c539f45f4a87310c0a1", "4dd64087604043be82f8c9e03956c4de", "aafb4969e88e4615bb69393ac80dd6a8"]} id="epfnL59kioOn" outputId="c2357bc0-c88a-4156-dc98-2f4352f78d6b"
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


# + [markdown] id="Cws-Xx78DyOz"
# #Part #3, Clustering

# + [markdown] id="CsnWf8KnJonE"
# #Find the optimum number of clusters
#
# # The optimum number of clusters will be determined based on specific evaluation metrics which will quantify the performance of the clustering algorithms. Since there is no definite set number of clusters to create, we will be using a couple of different evaluation metrics to determine the optimum number of clusters. These metrics are the Silhouette Coefficient and the Davies-Bouldin Score.
# # These metrics each have their own advantages and disadvantages. The choice to use either one is purely subjective and another metric can be chosen as well.

# + id="M6tuNn3LjMKE"
def cluster_eval(y, x):
    """
    Prints the scores of a set evaluation metric. Prints out the max and min values of the evaluation scores.
    """
    
    # Creating a DataFrame for returning the max and min scores for each cluster
    df = pd.DataFrame(columns=['Cluster Score'], index=[i for i in range(2, len(y)+2)])
    df['Cluster Score'] = y
    
    print('Max Value:\nCluster #', df[df['Cluster Score']==df['Cluster Score'].max()])
    print('\nMin Value:\nCluster #', df[df['Cluster Score']==df['Cluster Score'].min()])
    
    # Plotting out the scores based on cluster count
    plt.figure(figsize=(16,6))
    plt.style.use('bmh')
    plt.plot(x,y)
    plt.xlabel('# of Clusters')
    plt.ylabel('Score')
    plt.show()


# + [markdown] id="HMq9FNWVJWUN"
# # In the following, higher score meant higher relevancy.
#

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="gJ_OYzQCjOPc" outputId="7cb02362-1934-494c-87b8-655069f1398a"
print("The Calinski-Harabasz Score (find max score):")
cluster_eval(ch_scores, cluster_cnt)

print("\nThe Silhouette Coefficient Score (find max score):")
cluster_eval(s_scores, cluster_cnt)

print("\nThe Davies-Bouldin Score (find minimum score):")
cluster_eval(db_scores, cluster_cnt)

# + [markdown] id="w4hEtu2HKPNa"
# #Running the Final Clustering Algorithm
#
# #With everything ready, we can finally discover the clustering assignments for each mentor and mentee candidate.

# + id="3JGpxXVhioTt"
# Instantiating HAC based on the optimum number of clusters found
hac = AgglomerativeClustering(n_clusters=3, linkage='complete')

# Fitting
hac.fit(df_pca)

# Getting cluster assignments
cluster_assignments = hac.labels_

# Assigning the clusters to each profile
df['Cluster #'] = cluster_assignments

vect_df['Cluster #'] = cluster_assignments

# + [markdown] id="TF--1X-DLjzK"
# #With the mock dataset,
# #Cluster#0, shown 3 mentors and 4 mentees in one clustering for the match-maker.
# #Cluster#1, shown 1 mentor and 1 mentee in one clustering
# # Cluster#2, shown 1 mentor and 0 mentee in one clustering

# + colab={"base_uri": "https://localhost:8080/", "height": 459} id="Tm9wTjEwHKes" outputId="05dd14f0-4b15-4db5-89dd-ea6577d3f010"
df.head(10)
