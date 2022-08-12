import os
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.model import MatcherSortSearch
from app.sentiment import sentiment_rank
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate
from app.schema import Feedback, FeedbackUpdate, FeedbackOptions

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.49.0",
    docs_url='/',
)

API.db = MongoDB()
API.matcher = MatcherSortSearch()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.get("/version")
async def version():
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections")
async def collections():
    return {"result": API.db.get_database_info()}


@API.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
    return {"result": API.db.read("Mentors", data)}


@API.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    return {"result": API.db.read("Mentees", data)}


@API.post("/create/mentor")
async def create_mentor(data: Mentor):
    try:
        return {"result": API.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/create/mentee")
async def create_mentee(data: Mentee):
    try:
        return {"result": API.db.create("Mentees", data.dict())} 
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentors", {"profile_id": profile_id}, data)}


@API.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentees", {"profile_id": profile_id}, data)}


@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    return {"result": API.matcher(n_matches, profile_id)}


@API.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    return {"result": API.db.read("Feedback", query.dict(exclude_none=True))}


@API.post("/create/feedback")
async def create_feedback(data: Feedback):
    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.create("Feedback", data_dict)}


@API.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    API.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}


@API.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}
