from fastapi import APIRouter
from app.data import MongoDB

Router = APIRouter(
    tags=["Matching Operations"],
)

Router.db = MongoDB()


@Router.post("/create/match")
async def create_match(mentor_id: str, mentee_id: str):
    """Insert a new mentor/mentee pairing into the collection
    <pre><code>
    @param mentor_id: str
    @param mentee_id: str
    @return JSON[Boolean] - success or failure of update</pre></code>"""
    return {"result": Router.db.upsert_to_set_array("Matches",
                                                    {"mentor_id": mentor_id},
                                                    {"mentee_ids": mentee_id})}


@Router.post("/delete/match")
async def delete_match(mentor_id: str, mentee_id: str):
    """Remove a mentor/mentee pairing from the collection
    <pre><code>
    @param mentor_id: str
    @param mentee_id: str
    @return JSON[Boolean] - success or failure of update</pre></code>"""
    return {"result": Router.db.delete_from_array("Matches",
                                                  {"mentor_id": mentor_id},
                                                  {"mentee_ids": mentee_id})}


@Router.post("/read/match")
async def get_match(user_id: str, user_type: str):
    """Retrieve all matching mentor/mentee objects for a given mentee/mentor
    <pre><code>
    @param user_id: str
    @param user_type: str
    @return JSON[Array[Mentor]] | JSON[Array[Mentee]]</pre></code>"""
    if user_type == "mentor":
        db_col = "Mentees"
        query = {"mentee_ids": {"$in": list(Router.db.first("Matches", {'mentor_id': user_id}))}}
    elif user_type == "mentee":
        db_col = "Mentors"
        query = {"mentor_id": {
            "$in": [mentor['mentor_id'] for mentor in Router.db.read("Matches", {'mentee_ids': user_id})]}}
    else:
        raise ValueError("get_match: user_type must be 'mentor' or 'mentee'")

    return {"result": Router.db.read(db_col, query)}
