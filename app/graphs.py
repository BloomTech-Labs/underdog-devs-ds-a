from altair import Chart, Color, Tooltip, X, Y
import pandas as pd
from pandas import DataFrame

from app.data import MongoDB


def title_fix(string: str) -> str:
    return string.title().replace("_", " ")


light_mode_props = {
    "width": 480,
    "height": 400,
    "padding": 24,
    "background": "#FFFFFF",
}
light_mode_config = {
    "legend": {
        "titleColor": "#000000",
        "labelColor": "#000000",
        "padding": 10,
    },
    "title": {
        "color": "#000000",
        "fontSize": 26,
        "offset": 30,
    },
    "axis": {
        "titlePadding": 20,
        "titleColor": "#000000",
        "labelPadding": 5,
        "labelColor": "#000000",
        "gridColor": "#AAAAAA",
        "tickColor": "#AAAAAA",
        "tickSize": 10,
    },
    "view": {
        "stroke": "#AAAAAA",
    },
}
dark_mode_props = {
    "width": 480,
    "height": 400,
    "padding": 24,
    "background": "#252525",
}
dark_mode_config = {
    "legend": {
        "titleColor": "#AAAAAA",
        "labelColor": "#AAAAAA",
        "padding": 10,
    },
    "title": {
        "color": "#AAAAAA",
        "fontSize": 26,
        "offset": 30,
    },
    "axis": {
        "titlePadding": 20,
        "titleColor": "#AAAAAA",
        "labelPadding": 5,
        "labelColor": "#AAAAAA",
        "gridColor": "#333333",
        "tickColor": "#333333",
        "tickSize": 10,
    },
    "view": {
        "stroke": "#333333",
    },
}


def stacked_bar_chart(df: DataFrame,
                      column_1: str,
                      column_2: str,
                      title: str,
                      dark=True) -> Chart:
    props = dark_mode_props if dark else light_mode_props
    config = dark_mode_config if dark else light_mode_config
    return Chart(
        df,
        title=title,
    ).mark_bar().encode(
        x=X(column_1, title=title_fix(column_1), sort="-y"),
        y=Y(f"count({column_1})"),
        color=Color(column_2, title="Legend"),
        tooltip=Tooltip([column_2, column_1, f"count({column_1})"])
    ).properties(**props).configure(**config)


def df_tech_stack_by_role(database: MongoDB) -> DataFrame:
    mentees = DataFrame(database.projection("Mentees", {
        "is_active": True,
        "validate_status": "approved",
    }, {"tech_stack": True}))
    mentees["role"] = "Mentee"
    mentors = DataFrame(database.projection("Mentors", {
        "accepting_new_mentees": True,
        "is_active": True,
        "validate_status": "approved",
    }, {"tech_stack": True}))
    mentors = mentors.explode(column="tech_stack")
    mentors["role"] = "Mentor"
    return pd.concat([mentees, mentors])


def df_meeting(database: MongoDB) -> DataFrame:
    meeting = DataFrame(database.read("Meetings"))
    return meeting


def df_mentor_mentee(database: MongoDB) -> DataFrame:
    mentees = DataFrame(database.read("Mentees"))
    mentees["role"] = "Mentee"
    mentors = DataFrame(database.read("Mentors"))
    mentors["role"] = "Mentor"
    return pd.concat([mentees, mentors])


def df_sentiments(database: MongoDB) -> DataFrame:
    feedback_data = DataFrame(database.read("Feedback"))
    sentiment_data = feedback_data.filter(['sentiment'])
    return sentiment_data
