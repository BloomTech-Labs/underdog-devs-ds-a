from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.schema import Mentor, MentorOptions, MentorUpdate

Router = APIRouter(
    tags=["Mentor Operations"],
)

Router.db = MongoDB()


@Router.post("/create/mentor")
async def create_mentor(data: Mentor):
    """Create a mentor
    <pre><code>
    @param data: JSON[Mentor]
    @return JSON[Boolean] - Indicates success or failure of document creation
    </pre></code>
    """
    try:
        return {"result": Router.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail="Profile ID must be unique.")


@Router.post("/read/mentor")
<<<<<<< HEAD
async def read_mentor(query: MentorOptions):
    """Displays mentor(s) who meet provided criteria. Displays all mentors if no input provided
    <pre><code>
    @param query: MentorOptions
    @return JSON[Array[Mentor]]</pre></code>"""
    return {"result": Router.db.read("Mentors", query.dict(exclude_none=True))}
=======
async def read_mentor(data: Optional[Dict] = None):
    """Displays mentor(s) who meet provided criteria.
    Displays all mentors if no input provided
    <pre><code>
    @param data: JSON[Optional[Dict]]
    @return JSON[Array[Mentor]]</pre></code>
    """
    return {"result": Router.db.read("Mentors", data)}
>>>>>>> main


@Router.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    """Updates a mentor
    <pre><code>
    @param profile_id: str
    @param update_data: JSON[MentorUpdate]
    @return JSON[Boolean] - Indicates success or failure of update
    </pre></code>
    """
    data = update_data.dict(exclude_none=True)
    return {
        "result": Router.db.update("Mentors", {"profile_id": profile_id}, data)
    }
