from typing import Optional, Dict

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.schema import Mentee, MenteeUpdate

Router = APIRouter(
    tags=["Mentee Operations"],
)

Router.db = MongoDB()


@Router.post("/create/mentee")
async def create_mentee(data: Mentee):
    try:
        return {"result": Router.db.create("Mentees", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@Router.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    return {"result": Router.db.read("Mentees", data)}


@Router.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    data = update_data.dict(exclude_none=True)
    return {"result": Router.db.update("Mentees", {"profile_id": profile_id}, data)}
