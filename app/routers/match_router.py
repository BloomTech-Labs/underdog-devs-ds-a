from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.data import MongoDB
from app.schema import MatchQuery, MatchUpdate

Router = APIRouter(tags=["Matching Operations"])
Router.db = MongoDB()


@Router.post("/create/match")
async def create_match(data: MatchUpdate):
    """Insert a new mentor/mentee pairing into the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match creation
    </pre></code>
    """
    result = Router.db.upsert_to_set_array(
        "Matches",
        {"mentor_id": data.mentor_id},
        {"mentee_ids": data.mentee_id, "mentee_archive": data.mentee_id},
    )
    return {"result": result}


@Router.post("/delete/match")
async def delete_match(data: MatchUpdate):
    """Remove a mentor/mentee pairing from the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of match removal
    </pre></code>
    """
    result = Router.db.delete_from_array(
        "Matches",
        {"mentor_id": data.mentor_id},
        {"mentee_ids": data.mentee_id},
    )
    return {"result": result}


def get_mentor_matches(profile_id: str, use_archive: bool = False) -> List[str]:
    """Retrieves of mentee ids matched with this mentor """
    mentor = Router.db.first("Matches", {"mentor_id": profile_id})
    return mentor["mentee_archive"] if use_archive else mentor["mentee_ids"]


def get_mentee_matches(profile_id: str, use_archive: bool = False) -> List[str]:
    """Retrieves mentor ids matched with this mentee """
    key = "mentee_ids" if not use_archive else "mentee_archive"
    mentors = Router.db.read("Matches", {key: profile_id})
    return [mentor["mentor_id"] for mentor in mentors]


@Router.post("/read/match")
async def get_match(data: MatchQuery):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param data: JSON[MatchQuery]
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>
    """
    if data.user_type == "mentor":
        collection = "Mentees"
        matches = get_mentor_matches(data.user_id)
    elif data.user_type == "mentee":
        collection = "Mentors"
        matches = get_mentee_matches(data.user_id)
    else:
        raise HTTPException(404, "user_type should be `mentor` or `mentee`")

    if Router.db.count(collection, {"profile_id": data.user_id}):
        user_query = {"profile_id": {"$in": matches}}
        return {"result": Router.db.read(collection, user_query)}
    else:
        raise HTTPException(404, f"Matches for user `{data.user_id}`, not found")


@Router.get("/matches/all")
async def read_all_matches():
    """Retrieves all matches"""
    return Router.db.read("Matches")
