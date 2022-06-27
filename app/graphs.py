import altair as alt
import pandas as pd


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


def feedback_window(dataframe):
    """Global average positivity
       feedback of all Mentors by Mentees.
       Sliding window on the bar chart to see
       a line progression of the selected window."""

    interval = alt.selection_interval(encodings=['x'])

    source = dataframe

    bar = alt.Chart(source).mark_bar().encode(
        x='datetime:T',
        y='vader_score:Q',
        color=alt.condition(interval, 'mentor_id:N',
                            alt.value('lightgray'))
    ).properties(
        width=900,
        selection=interval
    )
    mean_line = alt.Chart(source).mark_line(color='red').transform_window(
        # The field to average
        rolling_mean='mean(vader_score)',
        # The number of values before and after the current value to include.
        # frame default is [null, 0]
        # frame=[-9, 0]
    ).encode(
        x='datetime',
        y='rolling_mean:Q'
    ).properties(width=900
                 ).transform_filter(
        interval)
    return (bar & mean_line).configure_title(fontSize=20
                                             ).configure(background='#D9E9F0')


def mentor_feedback_individual(dataframe):
    """Bar graph of all feedback of Mentors,
       mouseover individual bar interactively
       shows the Mentor, positivity of feedback,
       by which Mentee, and the actual feedback
       given."""

    source = dataframe
    selection = alt.selection_multi(fields=['mentor_id'], on='mouseover', bind='legend')

    mentor_bar = alt.Chart(source,
                           title="Individual Feedback Positivity Scores About a Mentor"
                           ).mark_bar(
        ).encode(
        alt.X('datetime', title='Time'),
        alt.Y('vader_score', title='Positivity of Feedback by Mentees'),
        color=alt.condition(selection, 'mentor_id:N',
                            alt.value('lightgray')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[alt.Tooltip('mentor_id'),
                 alt.Tooltip('feedback_outcome'),
                 alt.Tooltip('mentee_id'),
                 alt.Tooltip('feedback')]
    ).configure_range(
        category={'scheme': 'dark2'}
    ).properties(
        width=900,
        selection=selection
    ).add_selection(
        selection
    )
    return mentor_bar.configure_title(fontSize=20
                                      ).configure(background='#D9E9F0'
                                                  ).interactive()
