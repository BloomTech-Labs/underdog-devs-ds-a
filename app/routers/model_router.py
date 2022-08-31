from app.routers.data_router import Router
from fastapi import APIRouter

Router = APIRouter(
    prefix="/model",
    tags=["Model Operations"]
)

@Router.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    return {"result": Router.matcher(n_matches, profile_id)}