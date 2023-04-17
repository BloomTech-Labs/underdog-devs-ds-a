from typing import Optional

from fastapi import APIRouter

from app.data import MongoDB
from app.graphs import df_tech_stack_by_role, stacked_bar_chart

Router = APIRouter(tags=["Graph Operations"])
Router.db = MongoDB()


@Router.get("/graph/tech-stack-by-role")
async def tech_stack_by_role(dark: Optional[bool] = True):
    """Tech Stack Count by Role, stacked bar chart
    <pre><code>
    @return JSON{graph: Altair.Chart, description: String}</pre></code>
    """
    return {
        "graph": stacked_bar_chart(
            df_tech_stack_by_role(Router.db),
            "tech_stack",
            "role",
            "Tech Stack Count by Role",
            dark=dark,
        ).to_dict(),
        "description": "Shows the mentor to mentee tech stack ratio.",
    }
