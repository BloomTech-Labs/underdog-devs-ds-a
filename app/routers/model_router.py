from fastapi import APIRouter

from app.data import MongoDB
from app.model import MatcherSortSearch

Router = APIRouter(
    tags=["Model Operations"],
)
Router.db = MongoDB()
Router.matcher = MatcherSortSearch()


@Router.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """Returns n_matches mentor profiles for mentee profile_id
    <pre><code>
    @param profile_id: str
    @param n_matches: Optional[int] = None
    @return JSON[Array[profile_id]]</pre></code>"""
    return {"result": Router.matcher(n_matches, profile_id)}
