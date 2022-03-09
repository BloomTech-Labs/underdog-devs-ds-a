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
# # This notebook is part#1, Vectorization, part#2 PCA, part#3 Clustering, and part#4 Test Search for the Best Model
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

# + colab={"base_uri": "https://localhost:8080/", "height": 337} id="eewKg9IMXApt" outputId="8f03a57b-a771-4ad0-add9-9e04ea0a2202"
raw_df.head()

# + [markdown] id="PBuEBFUL2ipZ"
# # Start preparing vectorization

# + id="leXa1oCgYDd1"
df = raw_df.drop(['ID', 'First Name', 'Last Name',
                                        'Gender', 'Time zone'],axis=1)

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="7F1JG-ujYNU6" outputId="633d38b8-20be-47ca-a934-3ca8d8648038"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 442} id="x83xzMyqesOo" outputId="b729cdd1-ed9f-40fb-f466-2fd8406fe082"
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
        


# + colab={"base_uri": "https://localhost:8080/"} id="MsfqUgDIexC5" outputId="62a3f7b9-fb0c-406f-b988-21a8b0c1d2f6"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 462} id="UhLOEJuGYj-O" outputId="54899c65-d66c-4cbf-93de-9424f2c17509"
# Creating a new DF that contains the vectorized words
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(df['Bios'])
df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
df_wrds

# + colab={"base_uri": "https://localhost:8080/", "height": 444} id="7wb8RYgRYonq" outputId="931c3eb5-f724-4781-e132-e6a5d7bbf0bd"
# Concatenating the words DF with the original DF
new_df = pd.concat([df, df_wrds], axis=1)

# Dropping the Bios because it is no longer needed in place of vectorization
new_df.drop('Bios', axis=1, inplace=True)

# Viewing the new DF
new_df

# + colab={"base_uri": "https://localhost:8080/"} id="bvbS942gZJ2b" outputId="117895ab-2e6b-495d-92d2-6c7800662da1"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 331} id="7Lx_kezmY16S" outputId="34810d79-bd8c-4d0d-af7e-81cec49488cd"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 101, "referenced_widgets": ["9718729385ef454eb37f77839f18ca66", "e90238ac924743bbaba64ac4e1188300", "e360ba4c9e9d4469b5e06d25ff98e66c", "5ada4d50fcc542e7ab49de9e9313c5a6", "971d6ab56ff44e9494674d640cbb9cdd", "467acfe7f0a74975ad17e70f2af04344", "fedf4cd3e666441bb7b7a536b4a72559", "2bc8c9b6dcb4423e9801764acec87d24", "ca7d7eb0d89145ffaf7a415e12a1bfdb", "7c698845b6cd45b0aa9cc7fa236de738", "821da5f350234779ae5a9d0e13019538"]} id="epfnL59kioOn" outputId="bba3a919-209d-4b0e-a5a2-2e027c5564d3"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="gJ_OYzQCjOPc" outputId="8fb8ee13-9d5d-4489-a3f1-b8e083f345ac"
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

# + colab={"base_uri": "https://localhost:8080/", "height": 459} id="Tm9wTjEwHKes" outputId="790b803d-4120-47b3-e8b5-a91439d2f0d9"
df.head(10)

# + [markdown] id="tBOwYcZmUzGT"
# #Part#4, search for best model

# + [markdown] id="nYGjn5dZNBZD"
# #Prepare to find out the best model 

# + id="kt2n4BRleXNA"
# Importing 3 models
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier

# + colab={"base_uri": "https://localhost:8080/"} id="i92fZdBXjVFP" outputId="45c75d65-eab5-4c82-9d09-0539ce7a5446"
# Assigning the split variables
X = vect_df.drop(["Cluster #"], 1)
y = vect_df['Cluster #']

# Train, test, split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# + [markdown] id="RKhAz9TPIroV"
# #Different model tests to find out best model

# + id="h8Otr22xjXt7"
# Dummy
dummy = DummyClassifier(strategy='stratified')

# KNN
knn = KNeighborsClassifier()

# SVM
svm = SVC(gamma='scale')

# NaiveBayes
nb = ComplementNB()

# Logistic Regression
lr = LogisticRegression()

# Adaboost
adab = AdaBoostClassifier()

# List of models
models = [dummy, knn, svm, nb, lr, adab]

# List of model names
names = ['Dummy', 'KNN', 'SVM', 'NaiveBayes', 'Logistic Regression', 'Adaboost']

# Zipping the lists
classifiers = dict(zip(names, models))

# + [markdown] id="9GBNXE0jIpu9"
# #The following result shown, the KNN is the best model
# #KNN Score: 1.0; most likely the mock data is only 10 observations that caused overfitting

# + colab={"base_uri": "https://localhost:8080/", "height": 642, "referenced_widgets": ["f102072028bb43d389b58df050bb6f22", "789e8a7882cc4d91a61074033db0f7fe", "ce0dcd30999242f78f2ca11f9f5cc165", "65d553d34c4d4052b2309de52a59a5fa", "4b7068b365db470284848d4147ee6df6", "983ed4624c7e4862bfd1fdc6894ee51c", "c0dfcce5889c47c4aa646411af876a23", "b3f7f839d6724b1c935575110a5d48f7", "bf4464e3e12d465f92006732194da72b", "c02f8ba78d64490987c8d05dbb8b3913", "552a90bb15a1468badbc686adff4c538"]} id="geXJtNVZje3v" outputId="d45807e4-9c3b-41e1-b2b1-7254aae0a963"
# Dictionary containing the model names and their scores
models_f1 = {}

# Looping through each model's predictions and getting their classification reports
for name, model in tqdm(classifiers.items()):
    # Fitting the model
    model.fit(X_train, y_train)
    
    print('\n'+ name + ' (Macro Avg - F1 Score):')
    
    # Classification Report
    report = classification_report(y_test, model.predict(X_test), output_dict=True)
    f1 = report['macro avg']['f1-score']
    
    # Assigning to the Dictionary
    models_f1[name] = f1
    
    print(f1)

# + colab={"base_uri": "https://localhost:8080/"} id="zu8fxlkvjh-p" outputId="2e76c74d-b77f-41c2-a5bd-a88d05dae3ba"
print(max(models_f1, key=models_f1.get), 'Score:', max(models_f1.values()))

# + [markdown] id="FqmHb6tsImJ8"
#
# # Then, work with web team on app file
#
# # It will be very interesting to use the client's existing excel file dataset to run experiments on all-the-above and refine to final codes to use. 

# + [markdown] id="3RfeuFf7HqlI"
# #END of best model search
