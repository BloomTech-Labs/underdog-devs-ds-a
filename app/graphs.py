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

    bar = alt.Chart(dataframe, title="Global Feedback & Average of Feedback Positivity"
                    ).mark_bar().encode(
        alt.X('datetime', title='Time'),
        alt.Y('vader_score', title='Positivity of Feedback by Mentees'),
        color=alt.condition(interval, 'mentor_full_name:N',
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
        y='mentor_progress:Q'
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
        color=alt.condition(selection, 'mentor_full_name:N',
                            alt.value('lightgray')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[alt.Tooltip('mentor_full_name'),
                 alt.Tooltip('feedback_outcome'),
                 alt.Tooltip('mentee_full_name'),
                 alt.Tooltip('feedback')]
    ).configure_range(
        category={'scheme': 'dark2'}
    ).properties(
        width=900,
        selection=selection
    ).add_selection(
        selection
    )

    return mentor_bar.configure_title(fontSize=26).configure(background='#D9E9F0').interactive()
