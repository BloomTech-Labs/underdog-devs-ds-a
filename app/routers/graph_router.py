from fastapi import APIRouter

from app.data import MongoDB
from app.graphs import stacked_bar_chart, df_tech_stack_by_role, df_meeting, \
    df_mentor_mentee


Router = APIRouter(
    tags=["Graph Operations"],
)
Router.db = MongoDB()


@Router.get("/graph/tech-stack-by-role")
async def tech_stack_by_role():
    """Tech Stack Count by Role, stacked bar chart
    <pre><code>
    @return JSON{graph: Altair.Chart, description: String}</pre></code>"""
    desc_para_final = "This graph shows the Mentor to Mentee tech stack ratio."
    return {
        "graph": stacked_bar_chart(
            df_tech_stack_by_role(Router.db),
            "tech_stack",
            "role",
            "Tech Stack Count by Role"
        ).to_dict(),
        "description": desc_para_final,
    }


@Router.get("/graph/meeting-topics")
async def meeting_topics():
    """Meeting subjects, stacked bar chart
    <pre><code>
    @return JSON{Altair.Chart}</pre></code>"""
    description = "This graph shows the different meeting topics between mentors and mentees."
    return {
        "graph": stacked_bar_chart(
            df_meeting(Router.db),
            "meeting_topic",
            "count(meeting_topic)",
            "Count of Meetings by Topic"
        ).to_dict(),
        "description": description,
    }


@Router.get("/graph/meetings-missed")
async def meetings_missed():
    """Meetings missed by mentee, stacked bar chart
    <pre><code>
    @return JSON{Altair.Chart}</pre></code>"""
    description = "This graph shows the total number of meetings missed by mentees."
    return {
        "graph": stacked_bar_chart(
            df_meeting(Router.db),
            "meeting_missed_by_mentee",
            "count(meeting_missed_by_mentee)",
            "Count of Meetings Missed by Mentee"
        ).to_dict(),
        "description": description,
    }


@Router.get("/graph/activity-status")
async def is_active():
    """Activity status for mentees and/or mentors, stacked bar chart
    <pre><code>
    @return JSON{Altair.Chart}</pre></code>"""
    description = "This graph shows the activity status of both mentees and mentors."
    return {
        "graph": stacked_bar_chart(
            df_mentor_mentee(Router.db),
            "is_active",
            "role",
            "Count of Mentors and Mentees"
        ).to_dict(),
        "description": description,
    }
