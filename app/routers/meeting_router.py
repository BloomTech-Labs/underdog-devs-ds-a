from typing import Optional, Dict

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.schema import Meeting, MeetingUpdate

Router = APIRouter(
    tags=["Meeting Operations"],
)

Router.db = MongoDB()


@Router.post("/create/meeting")
async def create_meeting(data: Meeting):
    """Creates a meeting
    <pre><code>
    @param data: JSON[Meeting]
    @return JSON[Boolean] - Indicates success or failure of document creation
    </pre></code>"""
    try:
        return {"result": Router.db.create("Meetings", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail="Meeting ID must be unique.")


@Router.post("/read/meeting")
async def read_meeting(data: Optional[Dict] = None):
    """Displays meeting(s) that meet provided criteria.
    Displays all meetings if no input provided
    <pre><code>
    @param data: JSON[Optional[Dict]]
    @return JSON[Array[Meeting]]
    </pre></code>"""
    return {"result": Router.db.read("Meetings", data)}


@Router.patch("/update/meeting/{meeting_id}")
async def update_meeting(meeting_id: str, update_data: MeetingUpdate):
    """Updates a meeting
    <pre><code>
    @param meeting_id: str
    @param update_data: JSON[MeetingUpdate]
    @return JSON[Boolean] - Indicates success or failure of update
    </pre></code>"""
    data = update_data.dict(exclude_none=True, exclude_unset=True)
    return {"result": Router.db.update(
        "Meetings", {"meeting_id": meeting_id}, data)}


@Router.delete("/delete/meeting/{meeting_id}")
async def delete_meeting(meeting_id: str):
    """Deletes meeting
    <pre><code>
    @param meeting_id: str
    @return JSON[JSON[meeting_id]]
    </pre></code>"""
    Router.db.delete("Meetings", {"meeting_id": meeting_id})
    return {"result": {"deleted": meeting_id}}
