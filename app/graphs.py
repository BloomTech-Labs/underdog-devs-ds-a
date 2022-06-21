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


def feedback(dataframe):
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
        frame=[-9, 0]
    ).encode(
        x='datetime',
        y='rolling_mean:Q'
    ).properties(width=900
    ).transform_filter(
        interval)
    return bar & mean_line


def mentor_feedback_progression(dataframe):
    """Graphs the review progression
       over time for a Mentor"""
    source = dataframe
    selection = alt.selection_multi(fields=['mentor_id'], on='mouseover', bind='legend')

    mentor_bar = alt.Chart(source).mark_bar().encode(
        x='datetime:T',
        y='vader_score:Q',
        color=alt.condition(selection, 'mentor_id:N',
                            alt.value('lightgray')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).properties(
        width=900,
        selection=selection
    ).add_selection(
        selection
    )

    highlight = alt.selection(type='single', on='mouseover', bind='legend',
                              fields=['mentor_id'], nearest=True)

    base = alt.Chart(source).encode(
        x='datetime:T',
        y='vader_score:Q',
        color='mentor_id:N'
    )

    points = base.mark_circle().encode(
        opacity=alt.value(0)
    ).add_selection(
        highlight
    ).properties(
        width=900
    )

    lines = base.mark_line().encode(
        x='datetime',
        y='mean(vader_score)',
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    ).transform_filter(selection)

    progression = (points + lines).interactive()

    return mentor_bar & progression
