from typing import Dict, Optional

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
    """Creates a mentee
    <pre><code>
    @param data: JSON[Mentee]
    @return JSON[Boolean] - Indicates success or failure of document creation
    </pre></code>
    """
    try:
        return {"result": Router.db.create("Mentees", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail="Profile ID must be unique.")


@Router.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    """Displays mentee(s) who meet provided criteria.
    Displays all mentees if no input provided
    <pre><code>
    @param data: JSON[Optional[Dict]]
    @return JSON[Array[Mentee]]</pre></code>
    """
    return {"result": Router.db.read("Mentees", data)}


@Router.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    """Updates a mentee
    <pre><code>
    @param profile_id: str
    @param update_data: JSON[MenteeUpdate]
    @return JSON[Boolean] - Indicates success or failure of update
    </pre></code>
    """
    data = update_data.dict(exclude_none=True)
    return {
        "result": Router.db.update("Mentees", {"profile_id": profile_id}, data)
    }
