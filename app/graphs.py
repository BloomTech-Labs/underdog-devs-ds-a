import pandas
from altair import Chart, Color, Y, X, Tooltip
from pandas import DataFrame

from app.data import MongoDB


def title_fix(string: str) -> str:
    return string.title().replace("_", " ")


def stacked_bar_chart(df: DataFrame, column_1: str, column_2: str) -> Chart:
    return Chart(
        df,
        title=f"{title_fix(column_1)} Count by {title_fix(column_2)}",
    ).mark_bar().encode(
        x=X(column_1, title=title_fix(column_1), sort="-y"),
        y=Y(f"count({column_1})"),
        color=Color(column_2, title=title_fix(column_2)),
        tooltip=Tooltip([column_2, column_1, f"count({column_1})"])
    ).properties(
        width=480,
        height=400,
        padding=24,
    ).configure(
        legend={"padding": 24},
        title={"fontSize": 20, "offset": 24},
        view={"stroke": "#FFF"},
    )


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
    return pandas.concat([mentees, mentors])


def meeting_chart(df, column_1, column_2):
    return Chart(
        df,
        title=f"{title_fix(column_1)}",
    ).mark_bar().encode(
        x=X(column_1, title=title_fix(column_1), sort="-y"),
        y=Y(f"count({column_1})"),
        color=Color(column_1, title=title_fix(f"Legend")),
        tooltip=Tooltip([column_2, column_1, f"count({column_1})"])
    ).properties(
        width=480,
        height=400,
        padding=24,
    ).configure(
        legend={"padding": 24},
        title={"fontSize": 20, "offset": 24},
        view={"stroke": "#FFF"},
    )


def topic_chart(df, column_1, column_2):
    return Chart(
        df,
        title=f"{title_fix(column_1)}",
    ).mark_bar().encode(
        x=X(column_1, title=title_fix(column_1), sort="-y"),
        y=Y(f"count({column_1})"),
        color=Color(column_2, title='Count'),
        tooltip=Tooltip([column_2, column_1, f"count({column_1})"])
    ).properties(
        width=480,
        height=400,
        padding=24,
    ).configure(
        legend={"padding": 24},
        title={"fontSize": 20, "offset": 24},
        view={"stroke": "#FFF"},
    )


def activity_chart(df, column_1, column_2):
    return Chart(
        df,
        title=f"{title_fix(column_1)}",
    ).mark_bar().encode(
        x=X(column_1, title=title_fix(column_1), sort="-y"),
        y=Y(f"count({column_1})"),
        color=Color(column_2, title=title_fix(column_2)),
        tooltip=Tooltip([column_2, column_1, f"count({column_1})"])
    ).properties(
        width=480,
        height=400,
        padding=24,
    ).configure(
        legend={"padding": 24},
        title={"fontSize": 20, "offset": 24},
        view={"stroke": "#FFF"},
    )
