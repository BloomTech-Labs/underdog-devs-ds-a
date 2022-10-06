from fastapi import APIRouter

from app.data import MongoDB
from app.graphs import stacked_bar_chart, df_tech_stack_by_role, meeting_chart, df_meeting_topics, df_is_active, \
    activity_chart

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
        ).to_dict(),
        "description": desc_para_final,
    }


@Router.get("/graph/meeting-topics")
async def meeting_topics():
    """Meeting subjects, stacked bar chart
    <pre><code>
    @return JSON{Altair.Chart}</pre></code>"""
    description = "This graph shows something."
    return {
        "graph": meeting_chart(
            df_meeting_topics(Router.db),
            "meeting_topic",
            "count(meeting_topic)",
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
        "graph": meeting_chart(
            df_meeting_topics(Router.db),
            "meeting_missed_by_mentee",
            "count(meeting_missed_by_mentee)",
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
        "graph": meeting_chart(
            df_meeting_topics(Router.db),
            "meeting_missed_by_mentee",
            "count(meeting_missed_by_mentee)",
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
        "graph": activity_chart(
            df_is_active(Router.db),
            "is_active",
            "role",
        ).to_dict(),
        "description": description,
    }
