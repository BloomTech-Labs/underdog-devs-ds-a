from app.data import MongoDB
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

from category_encoders import OrdinalEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, plot_confusion_matrix, confusion_matrix, ConfusionMatrixDisplay

db = MongoDB("UnderdogDevs")
mentees = pd.DataFrame(db.read("Mentees"))
mentees.columns = ['mentee_' + c for c in mentees.columns]
mentors = pd.DataFrame(db.read("Mentors"))
mentors.columns = ['mentor_' + c for c in mentors.columns]
feedbacks = pd.DataFrame(db.read("Feedbacks"))

df = pd.merge(feedbacks, mentees, on='mentee_profile_id')
df = pd.merge(df, mentors, on='mentor_profile_id')

new_df = pd.DataFrame()
new_df['subject_indicator'] = df["mentee_subject"] == df["mentor_subject"]
new_df['experience_level_indicator'] = df["mentee_experience_level"] == df["mentor_experience_level"]
new_df['pair_programming_indicator'] = df['mentee_pair_programming'] == df['mentor_pair_programming']
new_df['industry_knowledge_indicator'] = df['mentor_industry_knowledge']
new_df['state_indicator'] = (df['mentee_state'] == df['mentor_state'])
new_df['mentee_formerly_incarcerated'] = df['mentee_formerly_incarcerated']
new_df['mentee_underrepresented_group'] = df['mentee_underrepresented_group']
new_df['mentee_low_income'] = df['mentee_low_income']

target = df['feedback']

X_train, X_val, y_train, y_val = train_test_split(new_df, target, test_size=0.2)

print(y_train.value_counts(normalize=True))
baseline = y_train.value_counts(normalize=True).max()
print('baseline: ', baseline)

model_rf = make_pipeline(
    OrdinalEncoder(),
    SimpleImputer(),
    RandomForestClassifier(n_jobs=-1, random_state=42)
)

model_rf.fit(X_train, y_train)
print('train accuracy score:', accuracy_score(y_train, model_rf.predict(X_train)))
print('val accuracy score:', accuracy_score(y_val, model_rf.predict(X_val)))

clf = make_pipeline(
    OrdinalEncoder(),
    SimpleImputer(),
    RandomForestClassifier(n_jobs=-1, random_state=42)
)
param_grid = {
    'randomforestclassifier__n_estimators': range(60, 200, 5),
    'randomforestclassifier__max_depth': range(5, 30, 2),
    'randomforestclassifier__min_samples_split': range(2, 10, 1)
}

model_rfrs = RandomizedSearchCV(
    clf,
    param_distributions=param_grid,
    n_jobs=-1,
    cv=2,
    verbose=1,
    n_iter=300
)

model_rfrs.fit(X_train, y_train)

best_score = model_rfrs.best_score_
best_param = model_rfrs.best_params_

print('best score for model: ', best_score)
print('best param for model: ', best_param)

train_accuracy1 = accuracy_score(y_train, model_rfrs.predict(X_train))
val_accuracy1 = accuracy_score(y_val, model_rfrs.predict(X_val))

print('train accuracy ', train_accuracy1)
print('val accuracy ', val_accuracy1)

'''
plot_confusion_matrix(
model_rfrs,
    X_train,
    y_train,
    values_format='.0f',
    display_labels=['Fair', 'Poor', 'Very Good']
)
'''

ConfusionMatrixDisplay.from_estimator(
    model_rfrs,
    X_train,
    y_train,
    values_format='.0f',
    display_labels=['Fair', 'Poor', 'Very Good']
)
plt.show()

print(y_val.value_counts())
ConfusionMatrixDisplay.from_estimator(
    model_rfrs,
    X_val,
    y_val,
    values_format='.0f',
    display_labels=['Fair', 'Poor', 'Very Good']
)
plt.show()

importances = model_rf.named_steps['randomforestclassifier'].feature_importances_
df_importances = pd.DataFrame(data=importances, index=X_train.columns, columns=['importance'])
rcParams.update({'figure.autolayout': True})
sorted_importances = df_importances.abs().sort_values(by=['importance'])
sorted_importances.tail(10).plot.barh()
plt.show()

important_indicators = list(df_importances.abs().sort_values(by=['importance'], ascending=False).index)
important_mentee_mentor_matching_features = []
for ind in important_indicators:
    if ind.find('indicator') != -1:
        important_mentee_mentor_matching_features.append(ind[:-10])
print(important_mentee_mentor_matching_features)