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

# + [markdown] id="xw3evre_j-88"
# # Objective: Predict % of Mentees that might leave Underdog Devs

# + [markdown] id="wq0fn_takVd_"
# ### What metrics would be helpful to predict this?
#
# - Number of support (customer service) tickets created
# - Length of time with Underdog Devs
# - Sessions attended overall
# - Sessions attended per week
# - Time commitment (suggested intake data point from Nigel's excel sheet)
# - Days available (suggested intake data point from Nigel's excel sheet)
# - ... Plus more that I haven't thought of...

# + [markdown] id="OrS_PK2cm34I"
# ### Why is this relevant?
#
# - Admin could anticipate when mentees might leave (and how many people might leave per month). This could help so admin is not left scrambling trying to solve mentor/mentee matching issues
# - This is probably not super relevant at the moment, but perhaps if Underdog Devs has many hundreds (or thousands) of mentees in the future then this data could be more useful.
#

# + id="KfzHfapujAur"
# Generate Mock Data

import random as r
import pandas as pd
import datetime


def random_date(start_y, start_m, start_d, end_y, end_m, end_d):
    start_date = datetime.date(start_y, start_m, start_d)
    end_date = datetime.date(end_y, end_m, end_d)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = r.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def percent_true(percent: int) -> bool:
    return r.randint(1, 100) <= percent


def get_status():
    if percent_true(90):
        if percent_true(55):
            return 'graduated'
        else:
            return 'active'
    return 'left'


def get_date_joined(status):
    if status == 'left':
        return random_date(2020, 1, 1, 2021, 11, 1)
    if status == 'graduated':
        return random_date(2020, 1, 1, 2021, 4, 1)
    if status == 'active':
        return random_date(2021, 9, 1, 2022, 1, 29)


def get_cst_val(status):  # purposefully skewing data
    if status == 'graduated':
        return r.randint(1, 4)
    if status == 'active':
        return r.randint(1, 2)
    return r.randint(3, 10)


def hrs(status):  # purposefully skewing data
    if status == 'graduated':
        return r.randrange(15, 40, 5)
    if status == 'active':
        return r.randrange(10, 40, 5)
    return r.randrange(5, 30, 5)


def sessions(status):  # purposefully skewing data
    if status == 'graduated':
        return r.randint(10, 40)
    if status == 'active':
        return r.randint(15, 20)
    return r.randint(1, 15)


def no_days(status):  # purposefully skewing data
    if status == 'graduated':
        return r.randint(2, 6)
    if status == 'active':
        return r.randint(3, 6)
    return r.randint(1, 3)


def departure_date(date_joined, status, no_sessions):
    if status == 'graduated':
        days = r.randint(90, 240)
        duration = datetime.timedelta(days=days)
        departure_date = date_joined + duration
        return departure_date
    if status == 'active':
        return None
    if 0 < no_sessions <= 2:
        days = r.randint(14, 42)
    elif 2 < no_sessions <= 4:
        days = r.randint(28, 54)
    elif 4 < no_sessions <= 6:
        days = r.randint(42, 70)
    elif 6 < no_sessions <= 8:
        days = r.randint(56, 84)
    elif 8 < no_sessions <= 10:
        days = r.randint(70, 112)
    elif 10 < no_sessions <= 15:
        days = r.randint(84, 140)
    duration = datetime.timedelta(days=days)
    departure_date = date_joined + duration
    return departure_date


class Mentee:

    def __init__(self):
        self.profile_id = 'E' + str(r.randint(1000000, 70000000000000))
        self.status = get_status()
        self.date_joined = get_date_joined(self.status)
        self.cust_serv_tickets = get_cst_val(self.status)
        self.time_commitment = hrs(self.status)  # hours/week
        self.no_sessions = sessions(self.status)
        self.days_available = no_days(self.status)  # days/week, max is Mon-Sat
        self.departure_date = departure_date(self.date_joined,
                                             self.status,
                                             self.no_sessions)

    @classmethod
    def to_df(cls, num_rows):
        return pd.DataFrame(vars(cls()) for _ in range(num_rows))



# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="nI5bUwlTvYzI" outputId="f82df65b-6129-4443-925f-6c33a2851232"
mentee = Mentee()
mentee_df = mentee.to_df(5000)
mentee_df[mentee_df['status'] == 'left'].head()


# + colab={"base_uri": "https://localhost:8080/"} id="1MGBM5MIvfTB" outputId="9bd8d383-b9ca-406d-ba95-734f2bb35060"
mentee_df['status'].value_counts()


# + [markdown] id="9uQ1IFS847Eu"
# # Feature Engineer a Duration Column

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="6-yjAtC33nrQ" outputId="b3f1efdc-0b1e-45c1-f86e-f904a8c40b40"
year = datetime.datetime.today().year
month = datetime.datetime.today().month
day = datetime.datetime.today().day
today = datetime.date(year=year, month=month, day=day)
mentee_df['today'] = today
mentee_df.head()


# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="gdFw9OSQ5MJA" outputId="3fd40496-9210-4fde-f96e-02e248f66336"
def get_duration(row):
    if row['status'] == 'active':
        duration = row['today'] - row['date_joined']
    else:
        duration = row['departure_date'] - row['date_joined']
    return duration

mentee_df['duration'] = mentee_df.apply(get_duration, axis=1)
mentee_df.head()


# + [markdown] id="_9LYHmIzFGHe"
# # We will need 2 separate models to compute attrition rate
#
# - First, a classification model for the active mentees
# - Second, a regression model that predicts duration

# + [markdown] id="Nj4CtapgRf-t"
# # Model 1: Classification

# + id="MamFlb8UGOSM"
def make_y_val(row):
    if row['status'] == 'active':
        num = 2
    if row['status'] == 'graduated':
        num = 1
    if row['status'] == 'left':
        num = 0
    return num



# + colab={"base_uri": "https://localhost:8080/"} id="T0hXVjUs_15O" outputId="76d347bb-d839-4221-df96-14aef1a25e90"
mentee_df_all_c = mentee_df.copy()  # '_c' for classification
mentee_df_all_c = mentee_df_all_c[['cust_serv_tickets', 'no_sessions',
                                   'time_commitment', 'days_available',
                                   'status']]

# Create numerical y value
mentee_df_all_c['y'] = mentee_df_all_c.apply(make_y_val, axis=1)
mentee_df_all_c.drop(columns='status', inplace=True)

# Drop rows of 'active' mentees
mentee_df_c = mentee_df_all_c[mentee_df_all_c['y'] != 2]
mentee_df_c['y'].value_counts()


# + colab={"base_uri": "https://localhost:8080/"} id="7DkGHOqYIJiE" outputId="334d0bf3-2fbb-4b67-e577-a0a6558c2d85"
mentee_df_c.dtypes


# + colab={"base_uri": "https://localhost:8080/", "height": 143} id="IYsEt22bKDKi" outputId="a6b174d8-ccc9-42be-b66e-7b3dffa94662"
mentee_df_c.head(3)


# + [markdown] id="aIBuh0YYKQll"
# ## Check Baseline Accuracy
#
# - i.e. always predict the mentee will graduate

# + colab={"base_uri": "https://localhost:8080/"} id="E2dR74D2KUGG" outputId="64bbce0a-6bc7-46e1-feb1-3bf52d856d59"
print('Baseline Accuracy:',
      mentee_df_c['y'].value_counts(normalize=True).max())


# + id="YaS1Bn_yMcr0"
# Create X and y
y = mentee_df_c['y']
X = mentee_df_c.drop(columns='y')


# + [markdown] id="dHQkdq2PPGam"
# ## Split into Train and Validation Set

# + id="JAypqN-sPJLl"
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)


# + colab={"base_uri": "https://localhost:8080/"} id="7q_BzdhNPdvB" outputId="b222b9b5-0377-4f58-dff4-ea1251d65d57"
y_train.value_counts()


# + colab={"base_uri": "https://localhost:8080/"} id="ii2_l_8LPiZO" outputId="2049256b-c8db-4d5b-dd1e-c1d100e8dc12"
y_val.value_counts()


# + [markdown] id="mfyc731nKLr1"
# ## Build Model

# + id="Cy0OD7ygKF32"
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
rfc = RandomForestClassifier()

param_grid = {
    "max_depth": [15, 20, 25, 30, 35, 40, 45, 50],
    "n_estimators": [10, 20, 30]
}

rfc_model = RandomizedSearchCV(rfc,
                               param_distributions=param_grid,
                               n_iter=15,
                               n_jobs=-1,
                               cv=3,
                               verbose=1)


# + colab={"base_uri": "https://localhost:8080/"} id="UW0sKrtbMwRW" outputId="82a09e6d-91a9-4f40-f3d8-ffe12efcaf8f"
rfc_model.fit(X_train, y_train)


# + colab={"base_uri": "https://localhost:8080/"} id="JtQVgiFPM2OY" outputId="a7952d89-3bd7-4dba-ae2b-1b607abc2dbe"
rfc_model.best_score_


# + colab={"base_uri": "https://localhost:8080/"} id="o_-Gut6ZR3Fk" outputId="eeb261d9-ad52-4d07-bf5c-e2209619b53c"
rfc_model.best_params_


# + [markdown] id="QyfnJtJAPv6t"
# ## Test Model On Held Back Data (validation set)

# + colab={"base_uri": "https://localhost:8080/"} id="MbBZXfcWPvrn" outputId="de58a29a-dc00-4a8d-d8bd-f7656f586d4a"
from sklearn.metrics import accuracy_score
val_predictions = rfc_model.predict(X_val)
accuracy_score(val_predictions, y_val)


# + [markdown] id="TYdLgSFUbzxs"
# ## Filter data to 'active' mentees

# + colab={"base_uri": "https://localhost:8080/"} id="b_vMCjkgN5OO" outputId="f594dd83-93f1-4b22-d660-46e01ad79717"
# 2: active, 1: graduated, 0: left
mentee_df_all_c['y'].value_counts()


# + colab={"base_uri": "https://localhost:8080/"} id="eEIebBT9b9c7" outputId="6e857129-2ccc-4999-c89c-865b669ee058"
mentee_df_active = mentee_df_all_c[mentee_df_all_c['y'] == 2].copy()
mentee_df_active['y'].value_counts()


# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="y_QkyCUKeT0v" outputId="2cadaec1-7620-488a-e36b-2f80d1c71059"
mentee_df_active.head()


# + [markdown] id="umL67dG8cfzM"
# ## Use classification model to predict the outcome of the active mentees

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="VAYaeF5BcWWs" outputId="14b8f615-af78-4cec-f854-8118a6bba09c"
X = mentee_df_active.drop(columns='y')
pred_outcome = rfc_model.predict(X)
mentee_df_active['pred_outcome'] = pred_outcome
mentee_df_active.head()


# + colab={"base_uri": "https://localhost:8080/"} id="Gk3G4mpFdSEq" outputId="d248cbcc-b08d-44e5-e00a-74a84cd03eca"
mentee_df_active['pred_outcome'].value_counts()


# + [markdown] id="b0tslPmuRkZv"
# # Model 2: Regression

# + [markdown] id="bxZSJ7QzpXc2"
# ## First, build a model based on the mentees who left, to predict how long they stay before leaving

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="z4uvfG6ypk74" outputId="8a48182b-2ced-44ba-9171-4e9353eafc5e"
mentee_df_left = mentee_df[mentee_df['status'] == 'left'].copy()
mentee_df_left.head()


# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="ZyxcezQappac" outputId="22d2dc27-7baf-40ab-8bbe-d82f0913ee5f"
# Convert duration to days, this is our y value
mentee_df_left['duration'] = mentee_df_left['duration'].dt.days
mentee_df_left.head()


# + id="8fsGK1G_qK8k"
mentee_df_left = mentee_df_left[['cust_serv_tickets', 'time_commitment',
                                 'no_sessions', 'days_available', 'duration']]

# Create X and y
y = mentee_df_left['duration']
X = mentee_df_left.drop(columns='duration')


# + [markdown] id="S7b2sXFps0_L"
# ## Build model to predict mentee duration based on mentees who left

# + id="TwKTOTcete2F"
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)


# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="PLbeFencxc-V" outputId="c9b65f5b-e6c9-4c6f-f069-af039288d701"
X_train.head()


# + id="Mr7jljGYte2I"
poly_features = poly.fit_transform(X)


# + id="0NvXSym5tON4"
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)


# + colab={"base_uri": "https://localhost:8080/"} outputId="f77616b4-fabf-485d-8cc0-a0aeeae61ea4" id="l-xHfZVwte2L"
poly_reg_model = LinearRegression()
poly_reg_model.fit(X_train, y_train)


# + [markdown] id="AWaL6AvLtyu7"
# ## Test Model On Held Back Data (validation set)

# + colab={"base_uri": "https://localhost:8080/"} id="3WZIu-eX6mlL" outputId="f181e938-95f3-4987-e24f-bb6d9b98996f"
from sklearn import metrics
import numpy as np
val_predictions = poly_reg_model.predict(X_val)
print('Mean Absolute Error (MAE):',
      metrics.mean_absolute_error(val_predictions, y_val))
print('R Squared:', metrics.r2_score(val_predictions, y_val))


# + [markdown] id="iv6LquW-u8QW"
# ### Basically, the model's predictions are off by about __ [MAE] __ on average.
# - MAE will change with each runtime but in my case it says 9.8

# + colab={"base_uri": "https://localhost:8080/"} id="z405F5IfuY3-" outputId="2d0142fe-7a3d-4dc4-c16e-e2200626100a"
poly_reg_model.coef_


# + [markdown] id="TR9QtNgDv5Va"
# ## Now we filter the earlier dataframe for mentees who are predicted to leave

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="Hkazi9YywAhb" outputId="1656a1a7-1904-4771-fc67-7013ef33513f"
# Currently active mentees that the classification
# model predicts will leave
mentee_df_leaving_predictions = \
    mentee_df_active[mentee_df_active['pred_outcome'] == 0].copy()

mentee_df_leaving_predictions.head()


# + [markdown] id="wvuZrxeTwrQF"
# ## Now apply the regression model to predict duration

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="48kICFCDwn_d" outputId="eb4fac56-0cd0-4790-dc70-796986874e81"
mentee_df_leaving_predictions = \
    mentee_df_leaving_predictions[['cust_serv_tickets',
                                   'time_commitment',
                                   'no_sessions',
                                   'days_available']].copy()

duration_pred = poly_reg_model.predict(mentee_df_leaving_predictions)
mentee_df_leaving_predictions['duration_pred'] = duration_pred
mentee_df_leaving_predictions.head()


# + [markdown] id="WtOkY2C885gg"
# ## Now we add the predicted duration onto each mentee's start date

# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="MKPTRhTixnT_" outputId="12a7589d-9e8a-4f71-f044-ecf3c7de6c95"
mentee_df.head()


# + id="RlUaCeqh9B1S"
leaving_predictions = list(mentee_df_leaving_predictions.index.values)
mentee_df['duration_pred'] = ''
for i in range(len(mentee_df)):
    if i in leaving_predictions:
        duration_pred_ = mentee_df_leaving_predictions.at[i, 'duration_pred']
        date_joined = mentee_df.at[i, 'date_joined']
        mentee_df_leaving_predictions.at[i, 'pred_leave_date'] = \
            date_joined + datetime.timedelta(days=duration_pred_)


# + colab={"base_uri": "https://localhost:8080/", "height": 206} id="3unoI3d89N6i" outputId="f9c13bf6-2eb0-4960-eeed-4bc71dc632c5"
mentee_df_leaving_predictions.head()


# + [markdown] id="Ymhi05oHAHX_"
# ## How many mentees are predicted to leave in March 2022?

# + colab={"base_uri": "https://localhost:8080/", "height": 300} id="_j_B9-4S-eAR" outputId="0a82fc27-7d55-43cc-b775-5951098763d2"
mentee_df_leaving_predictions['pred_leave_date'] = \
    pd.to_datetime(mentee_df_leaving_predictions['pred_leave_date'])

no_mentees_pred_to_leave_each_month = \
    mentee_df_leaving_predictions.groupby(pd.Grouper(key='pred_leave_date',
                                                     freq='M')).count()

no_mentees_pred_to_leave_each_month


# + [markdown] id="iIfzm_7kCEGL"
# - Each row is 1 month
# - The count, which is shown in each column, is the total number of mentees that are predicted to leave in that particular month
# - Data will change with each runtime, but it currently shows 72 mentees will leave in March 2022

# + colab={"base_uri": "https://localhost:8080/"} id="93GDgprbATf4" outputId="c817f8d6-ea59-43fe-8a17-4e48c62079fe"
# Total active mentees
total_active_mentees = mentee_df_active.shape[0]
total_active_mentees


# + colab={"base_uri": "https://localhost:8080/"} id="6NMayXMZCqBr" outputId="e2f9150f-36aa-44a3-ec5d-7172dd006d93"
march_number = no_mentees_pred_to_leave_each_month.iloc[2, 1]
march_number


# + [markdown] id="DhiamQxaDppv"
# # Attrition for March 2022

# + colab={"base_uri": "https://localhost:8080/", "height": 35} id="5z1BPYO3DTvp" outputId="7ad904d0-1e18-4fa9-97ff-d78855d13586"
attrition = march_number / total_active_mentees
attrition = "{:.2%}".format(attrition)
attrition


# + [markdown] id="QY7O2Iz6KeES"
# ### Overall, the mock data and models are not perfect. The main point of the notebook is more to provide a rough outline for how the process could look in the future.

# + id="XDbSIKZtDiWh"

