from fastapi import APIRouter
from app.data import MongoDB
from app.schema import FeedbackOptions, FeedbackUpdate
from app.sentiment import sentiment_rank

Router = APIRouter(
    prefix="/feedback",
    tags=["Feedback Operations"],
)

Router.db = MongoDB()


@Router.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    return {"result": Router.db.read("Feedback", query.dict(exclude_none=True))}


@Router.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    Router.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}


@Router.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}
