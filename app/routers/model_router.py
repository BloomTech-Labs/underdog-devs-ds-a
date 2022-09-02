from fastapi import APIRouter
from app.data import MongoDB
from app.schema import Feedback
from app.sentiment import sentiment_rank

Router = APIRouter(
    tags=["Model Operations"],
)
Router.db = MongoDB()


@Router.post("/create/feedback")
async def create_feedback(data: Feedback):
    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.create("Feedback", data_dict)}


@Router.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    return {"result": Router.matcher(n_matches, profile_id)}
