from fastapi import APIRouter

from app.data import MongoDB
from app.schema import Match

Router = APIRouter(tags=["Matching Operations"])
Router.db = MongoDB()


@Router.post("/match")
async def create_match(data: Match):
    """Insert a new mentor/mentee pairing into the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match creation
    </pre></code>
    """
    Router.db.collection("Mentors").update_one(
        {"profile_id": data.mentor_id},
        {"$push": {"matches": data.mentee_id}}
    )
    Router.db.collection("Mentees").update_one(
        {"profile_id": data.mentee_id},
        {"$push": {"matches": data.mentor_id}}
    )
    return {"result": data}


@Router.delete("/match")
async def delete_match(data: Match):
    """Remove a mentor/mentee pairing from the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match removal
    </pre></code>
    """
    Router.db.collection("Mentors").update_one(
        {"profile_id": data.mentor_id},
        {"$pull": {"matches": data.mentee_id}}
    )
    Router.db.collection("Mentees").update_one(
        {"profile_id": data.mentee_id},
        {"$pull": {"matches": data.mentor_id}}
    )
    return {"result": data}
