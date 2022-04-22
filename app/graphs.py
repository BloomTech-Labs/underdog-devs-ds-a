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
