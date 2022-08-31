from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.schema import Feedback, FeedbackUpdate, FeedbackOptions
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate
from app.sentiment import sentiment_rank

Router = APIRouter(
    prefix="/data",
    tags=["Data Operations"]
)


@Router.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
    return {"result": Router.db.read("Mentors", data)}

@Router.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    return {"result": Router.db.read("Mentees", data)}  #


@Router.post("/create/mentor")
async def create_mentor(data: Mentor):
    try:
        return {"result": Router.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")
    
@Router.post("/create/mentee")
async def create_mentee(data: Mentee):
    try:
        return {"result": Router.db.create("Mentees", data.dict())} 
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@Router.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": Router.db.update("Mentors", {"profile_id": profile_id}, data)}


@Router.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": Router.db.update("Mentees", {"profile_id": profile_id}, data)}

@Router.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    return {"result": Router.db.read("Feedback", query.dict(exclude_none=True))}


@Router.post("/create/feedback")
async def create_feedback(data: Feedback):
    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.create("Feedback", data_dict)}

@Router.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    Router.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}

@Router.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}