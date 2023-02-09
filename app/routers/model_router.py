from typing import Optional

from fastapi import APIRouter

from app.data import MongoDB
from app.model import MenteeMatcherSearch
from app.model import MentorMatcherSearch

Router = APIRouter(tags=["Match Suggestions"])
Router.db = MongoDB()
Router.mentee_matcher = MenteeMatcherSearch()
Router.mentor_matcher = MentorMatcherSearch()

@Router.post("/mentee-match/{profile_id}")
async def mentee_match(profile_id: str, n_matches: Optional[int] = None):
    """Returns mentor profiles for mentee profile_id
    <pre><code>
    @param profile_id: str
    @param n_matches: Optional[int] = None
    @return JSON[Array[profile_id]]</pre></code>
    """
    return {"result": Router.mentee_matcher(profile_id, n_matches)}

@Router.post("/mentor-match/{profile_id}")
async def mentor_match(profile_id: str, n_matches: Optional[int] = None):
    """Returns mentee profiles for mentor profile_id
    <pre><code>
    @param profile_id: str
    @param n_matches: Optional[int] = None
    @return JSON[Array[profile_id]]</pre></code>
    """
    return {"result": Router.mentor_matcher(profile_id, n_matches)}
