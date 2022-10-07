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
    @return JSON[Boolean] - success or failure of update</pre></code>"""
    data = data.dict()
    return {"result": Router.db.upsert_to_set_array("Matches",
                                                    {"mentor_id": data["mentor_id"]},
                                                    {"mentee_ids": data["mentee_id"]})}


@Router.post("/delete/match")
async def delete_match(data: MatchUpdate):
    """Remove a mentor/mentee pairing from the collection
    <pre><code>
    @param data: JSON[MatchUpdate]
    @return JSON[Boolean] - success or failure of update</pre></code>"""
    data = data.dict()
    return {"result": Router.db.delete_from_array("Matches",
                                                  {"mentor_id": data["mentor_id"]},
                                                  {"mentee_ids": data["mentee_id"]})}


@Router.post("/read/match")
async def get_match(query: MatchQuery):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param query: JSON[MatchQuery]
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>"""
    query = query.dict()
    if query["user_type"] == "mentor":
        db_col = "Mentees"
        query = {"mentee_ids": {"$in": list(Router.db.first("Matches", {"mentor_id": query["user_id"]}))}}
    elif query["user_type"] == "mentee":
        db_col = "Mentors"
        query = {"mentor_id": {
            "$in": [mentor["mentor_id"] for mentor in Router.db.read("Matches", {"mentee_ids": query["user_id"]})]}}
    else:
        raise ValueError("get_match: user_type must be 'mentor' or 'mentee'")

    return {"result": Router.db.read(db_col, query)}
