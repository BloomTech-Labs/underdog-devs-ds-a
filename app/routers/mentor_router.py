from fastapi import HTTPException, APIRouter
from pymongo.errors import DuplicateKeyError

from typing import Dict, Optional
from app.routers.data_router import Router
from app.schema import MentorUpdate, Mentor

Router = APIRouter(
    prefix="/mentor",
    tags=["Mentor Operations"]
)

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

