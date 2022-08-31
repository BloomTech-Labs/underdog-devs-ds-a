from fastapi import HTTPException, APIRouter
from pymongo.errors import DuplicateKeyError
from typing import Dict, Optional

from app.routers.data_router import Router
from app.schema import MenteeUpdate, Mentee

Router = APIRouter(
    prefix="/mentee",
    tags=["Mentee Operations"]
)

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

