import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.routers import (graph_router,
                         feedback_router,
                         match_router,
                         meeting_router,
                         mentee_router,
                         mentor_router,
                         model_router)

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.52.2",
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


@API.get("/version")
async def version():
    """API version and password
    <pre><code>
    @return: JSON[JSON[String,String]]</pre></code>
    """
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections")
async def collections():
    """Names of collections and the count of documents in each collection
    <pre><code>
    @return JSON[JSON[String,Integer]]</pre></code>
    """
    return {"result": API.db.get_database_info()}


for router in (mentor_router,
               mentee_router,
               feedback_router,
               graph_router,
               model_router,
               match_router,
               meeting_router):
    API.include_router(router.Router)
