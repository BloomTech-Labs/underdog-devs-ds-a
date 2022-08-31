import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.model import MatcherSortSearch
from app.routers import (mentor_router,
                         mentee_router,
                         data_router,
                         model_router,
                         graph_router)


API = FastAPI(
    title='Underdog Devs DS API',
    version="0.49.1",
    docs_url='/',
)

API.db = MongoDB()
API.matcher = MatcherSortSearch()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@API.post("/info", tags=["General Operations"])
async def info():
    return {"info": "API Information"}


@API.get("/version")
async def version():
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections")
async def collections():
    return {"result": API.db.get_database_info()}


for router in (mentor_router, mentee_router, data_router, model_router, graph_router):
    API.include_router(router.Router)