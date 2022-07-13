import altair as alt
import pandas as pd
import numpy as np
from app.vader_sentiment import vader_score, vader_compound_score
from fastapi import FastAPI
from app.data import MongoDB

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.46.2",
    docs_url='/',
)

API.db = MongoDB("UnderdogDevs")


def tech_stack_by_role(dataframe: pd.DataFrame):
    return alt.Chart(
        dataframe,
        title='Tech Stack by Role',
    ).mark_bar(opacity=0.7).encode(
        x=alt.X('count()', title=""),
        y=alt.Y('tech_stack', title=""),
        color=alt.Color('user_role', title="User Role"),
        tooltip=alt.Tooltip(list(dataframe.columns)),
    )


def mentor_feedback_dataframe():
    feedback_df = pd.DataFrame(API.db.read('Feedback'))
    mentee_df = pd.DataFrame(API.db.projection('Mentees', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentor_df = pd.DataFrame(API.db.projection('Mentors', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentee_df.rename(
        columns={
            'profile_id': 'mentee_id',
            'first_name': 'mentee_first_name',
            'last_name': 'mentee_last_name',
        },
        inplace=True)
    mentor_df.rename(
        columns={
            'profile_id': 'mentor_id',
            'first_name': 'mentor_first_name',
            'last_name': 'mentor_last_name',
        },
        inplace=True)
    mentor_df['mentor_full_name'] = mentor_df.mentor_first_name.str.cat(mentor_df.mentor_last_name, sep=" ")
    mentee_df['mentee_full_name'] = mentee_df.mentee_first_name.str.cat(mentee_df.mentee_last_name, sep=" ")
    df_1 = pd.merge(feedback_df, mentee_df, on='mentee_id', how='left')
    mentor_feedback_df = pd.merge(df_1, mentor_df, on='mentor_id', how='left')
    mentor_feedback_df['datetime'] = np.random.choice(  # will be removed once its regenerated
        pd.date_range('2020-01-01', '2022-01-01'),
        len(mentor_feedback_df))
    mentor_feedback_df['feedback_outcome'] = mentor_feedback_df['feedback'].apply(lambda x: vader_score(x))
    mentor_feedback_df['vader_score'] = mentor_feedback_df['feedback'].apply(lambda x: vader_compound_score(x))
    return mentor_feedback_df


def feedback_window(dataframe):
    """Global average positivity
       feedback of all Mentors by Mentees.
       Sliding window on the bar chart to see
       a line progression of the selected window."""

    interval = alt.selection_interval(encodings=['x'])

    bar = alt.Chart(dataframe, title="Global Feedback & Average of Feedback Positivity"
                    ).mark_bar().encode(
        alt.X('datetime', title='Time'),
        alt.Y('vader_score', title='Positivity of Feedback by Mentees'),
        color=alt.condition(interval, alt.Color('mentor_full_name:N',
                                                title="Mentor",
                                                legend=alt.Legend(orient="left")),
                            alt.value('lightgray'))
    ).properties(
        width=900,
        selection=interval
    )
    mean_line = alt.Chart(dataframe).mark_line(color='red').transform_window(
        # The field to average
        mentor_progress='mean(vader_score)',
        # The number of values before and after the current value to include.
        frame=[-9, 0]
    ).encode(
        alt.X('datetime', title='Time'),
        alt.Y("mean(vader_score)", title="Progress of Mentors")
    ).properties(
        width=900
    ).transform_filter(
        interval
    )

    return (bar & mean_line).configure_title(fontSize=20
                                             ).configure(background='#D9E9F0')


def mentor_feedback_individual(dataframe):
    """Bar graph of all feedback of Mentors,
       mouseover individual bar interactively
       shows the Mentor, positivity of feedback,
       by which Mentee, and the actual feedback
       given."""

    selection = alt.selection_multi(fields=['mentor_full_name'], on='mouseover', bind='legend')

    mentor_bar = alt.Chart(dataframe, title="Individual Feedback Positivity Scores About a Mentor").mark_bar().encode(
        alt.X('datetime', title='Time'),
        alt.Y('vader_score', title='Positivity of Feedback by Mentees'),
        color=alt.condition(selection, alt.Color('mentor_full_name:N',
                                                 title="Mentor",
                                                 legend=alt.Legend(orient="left")),
                            alt.value('lightgray')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[alt.Tooltip('mentor_full_name', title='Mentor'),
                 alt.Tooltip('feedback_outcome', title='Feedback Outcome'),
                 alt.Tooltip('mentee_full_name', title='Mentee'),
                 alt.Tooltip('feedback', title='Feedback Given')]
    ).configure_range(
        category={'scheme': 'dark2'}
    ).properties(
        width=900,
        selection=selection
    ).add_selection(
        selection
    )

    return mentor_bar.configure_title(fontSize=26).configure(background='#D9E9F0').interactive()
