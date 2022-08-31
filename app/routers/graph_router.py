from fastapi import APIRouter

from app.graphs import stacked_bar_chart, df_tech_stack_by_role


Router = APIRouter(
    prefix="/data",
    tags=["Graph Operations"]
)

@Router.get("/graph/tech-stack-by-role")
async def tech_stack_by_role():
    """ Tech Stack Count by Role - stacked bar chart
    Returns an Altair Chart in JSON format """
    return stacked_bar_chart(
        df_tech_stack_by_role(API.db),
        "tech_stack",
        "role",
    ).to_dict()