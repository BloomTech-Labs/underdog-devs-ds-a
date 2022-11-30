from fastapi import APIRouter

from app.data import MongoDB
from app.schema import MatchQuery, MatchUpdate

Router = APIRouter(
    tags=["Matching Operations"],
)

Router.db = MongoDB()


@Router.post("/create/match")
async def create_match(data: MatchUpdate):
    """Insert a new mentor/mentee pairing into the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match creation
    </pre></code>
    """
    return {
        "result": Router.db.upsert_to_set_array("Matches",
                                                {"mentor_id": data.mentor_id},
                                                {"mentee_ids": data.mentee_id})
    }


@Router.post("/delete/match")
async def delete_match(data: MatchUpdate):
    """Remove a mentor/mentee pairing from the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match removal
    </pre></code>
    """
    return {
        "result": Router.db.delete_from_array("Matches",
                                              {"mentor_id": data.mentor_id},
                                              {"mentee_ids": data.mentee_id})
    }


@Router.post("/read/match")
async def get_match(data: MatchQuery):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param data: JSON[MatchQuery]
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>
    """
    if data.user_type == "mentor":
        collection = "Mentees"
        user_query = {"profile_id": {"$in": Router.db.first(
            "Matches", {"mentor_id": data.user_id})['mentee_ids']}}
    elif data.user_type == "mentee":
        collection = "Mentors"
        user_query = {
            "profile_id": {
                "$in": [mentor["mentor_id"] for mentor in Router.db.read(
                    "Matches", {"mentee_ids": data.user_id})]
            }
        }
    else:
        raise ValueError("get_match: user_type must be 'mentor' or 'mentee'")

    return {"result": Router.db.read(collection, user_query)}
