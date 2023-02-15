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


def get_mentor_matches(profile_id: str) -> List[dict]:
    """Retrieves of mentees matched with this mentor """
    matched_ids = Router.db.first("Matches", {"mentor_id": profile_id})["mentee_ids"]
    return Router.db.read("Mentees", {"profile_id": {"$in": matched_ids}})


def get_mentee_matches(profile_id: str) -> List[dict]:
    """Retrieves mentors matched with this mentee """
    matches = Router.db.read("Matches", {"mentee_ids": profile_id})
    matched_ids = [match["mentor_id"] for match in matches]
    return Router.db.read("Mentors", {"profile_id": {"$in": matched_ids}})


@Router.post("/read/match")
async def get_match(data: MatchQuery):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param data: JSON[MatchQuery]
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>
    """
    if data.user_type == "mentor":
        return get_mentor_matches(data.user_id)
    elif data.user_type == "mentee":
        return get_mentee_matches(data.user_id)
    else:
        raise HTTPException(404, f"User type {data.user_type}, not found. Try 'mentor' or 'mentee'.")


@Router.get("/matches/all")
async def read_all_matches():
    """Retrieves all matches as ids """
    return Router.db.read("Matches")


@Router.get("/matches/all/obj")
async def read_all_matches_obj():
    """Retrieves all matches as objects"""
    all_matches = Router.db.read("Matches")
    return [{
        "mentor": Router.db.first("Mentors", {"profile_id": match["mentor_id"]}),
        "mentees": Router.db.read("Mentees", {"profile_id": {"$in": match["mentee_ids"]}}),
    } for match in all_matches]
