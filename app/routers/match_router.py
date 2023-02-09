from fastapi import APIRouter
from fastapi.exceptions import HTTPException

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
                                                {"mentee_ids": data.mentee_id,
                                                 "mentee_archive": data.mentee_id})
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


def get_match_ids(profile_id: str, profile_type: str, use_archive: bool = False) -> list:
    """Retrieves ids of mentees/mentors matched with profile id"""
    ids = []
    if profile_type == "mentor":
        if use_archive:
            ids = Router.db.first("Matches", {"mentor_id": profile_id})["mentee_archive"]
        else:
            ids = Router.db.first("Matches", {"mentor_id": profile_id})["mentee_ids"]
    elif profile_type == "mentee":
        if use_archive:
            ids = [mentor["mentor_id"] for mentor in Router.db.read(
                "Matches", {"mentee_archive": profile_id})]
        else:
            ids = [mentor["mentor_id"] for mentor in Router.db.read(
                "Matches", {"mentee_ids": profile_id})]

    return ids


@Router.post("/read/match")
async def get_match(data: MatchQuery):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param data: JSON[MatchQuery]
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>
    """
    if data.user_type == "mentor":
        collection = "Mentees"
    elif data.user_type == "mentee":
        collection = "Mentors"
    else:
        raise HTTPException(404, "user_type should be `mentor` or `mentee`")

    if Router.db.count(collection, {"profile_id": data.user_id}):
        match_ids = get_match_ids(data.user_id, data.user_type)
        user_query = {"profile_id": {"$in": match_ids}}
        return {"result": Router.db.read(collection, user_query)}
    else:
        raise HTTPException(404, f"user_id `{data.user_id}`, not found")
