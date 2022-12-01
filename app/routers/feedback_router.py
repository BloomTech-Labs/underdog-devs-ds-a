from fastapi import APIRouter
from app.data import MongoDB
from app.schema import FeedbackOptions, FeedbackUpdate, Feedback
from app.sentiment import apply_sentiment

Router = APIRouter(
    tags=["Feedback Operations"],
)

Router.db = MongoDB()


@Router.post("/create/feedback")
async def create_feedback(data: Feedback):
    """Creates feedback (with vadersentiment analysis)
    <pre><code>
    @param data: Feedback
    @return JSON[Boolean] - Indicates success or failure of feedback creation</pre></code>"""
    data_dict = data.dict(exclude_none=True)
    data_dict = apply_sentiment(data_dict)
    return {"result": Router.db.create("Feedback", data_dict)}


@Router.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    """Returns mentee feedback
    <pre><code>
    @param query: FeedbackOptions
    @return JSON[Array[Feedback]]</pre></code>"""
    return {"result": Router.db.read("Feedback", query.dict(exclude_none=True))}


@Router.patch("/update/feedback/{ticket_id}")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    """Updates feedback
    <pre><code>
    @param ticket_id: str
    @param update_data: FeedbackUpdate
    @return JSON[Boolean] - indicates success or failure of update</pre></code>"""
    data_dict = update_data.dict(exclude_none=True)
    data_dict = apply_sentiment(data_dict)
    return {"result": Router.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}


@Router.delete("/delete/feedback/{ticket_id}")
async def delete_feedback(ticket_id: str):
    """Deletes feedback
    <pre><code>
    @param ticket_id: str
    @return JSON[JSON[ticket_id]]</pre></code>"""
    Router.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}
