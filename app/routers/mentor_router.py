from typing import Optional, Dict

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.schema import Mentor, MentorUpdate

Router = APIRouter(
    tags=["Mentor Operations"],
)

Router.db = MongoDB()


@Router.post("/create/mentor")
async def create_mentor(data: Mentor):
    try:
        return {"result": Router.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@Router.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
    return {"result": Router.db.read("Mentors", data)}


@Router.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": Router.db.update("Mentors", {"profile_id": profile_id}, data)}
