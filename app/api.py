import os
from itertools import chain

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.routers import (graph_router,
                         match_router,
                         mentee_router,
                         mentor_router,
                         model_router)

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.55.2",
    docs_url='/',
)

API.db = MongoDB()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.get("/version", tags=["General Operations"])
async def version():
    """API version and password
    <pre><code>
    @return: JSON[JSON[String,String]]</pre></code>
    """
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections", tags=["General Operations"])
async def collections():
    """Names of collections and the count of documents in each collection
    <pre><code>
    @return JSON[JSON[String,Integer]]</pre></code>
    """
    return {"result": API.db.get_database_info()}


@API.get("/get/all", tags=["General Operations"])
async def get_all():
    mentees = API.db.read("Mentees")
    mentors = API.db.read("Mentors")
    return list(chain(mentees, mentors))


for router in (mentor_router,
               mentee_router,
               graph_router,
               model_router,
               match_router):
    API.include_router(router.Router)
