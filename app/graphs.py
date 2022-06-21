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
  line = alt.Chart(source).mark_line(color='red').transform_window(
      # The field to average
      rolling_mean='mean(vader_score)',
      # The number of values before and after the current value to include.
      frame=[-9, 0]
  ).encode(
      x='datetime',
      y='rolling_mean:Q'
  ).properties(width=900
  ).transform_filter(
      interval
  )
  return bar & line