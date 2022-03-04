from typing import Dict, Optional

from fastapi import FastAPI, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.data import MongoDB
from app.model import MatcherSortSearch

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.0.3",
    docs_url='/',
)


API.db = MongoDB("UnderdogDevs")
API.matcher = MatcherSortSearch()

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    """ Returns the current version of the API. """
    return {"result": API.version}


@API.get("/collections")
async def collections():
    """ Returns collection name and size of each collection. """
    return {"result": API.db.scan_collections()}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """ Creates a new record. """
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """ Returns array of records that exactly match the query. """
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """ Returns an array containing the query and updated data. """
    return {"result": API.db.update(collection, query, update_data)}


@API.post("/{collection}/search")
async def search(collection: str, user_search: str):
    """ Returns array of records that loosely match the search,
    automatically ordered by relevance. """
    return {"result": API.db.search(collection, user_search)}


@API.post("/match/{mentee_id}")
async def match(mentee_id: int, n_matches: int):
    """ Returns array of mentor matches for any given mentee_id. """
    return {"result": API.matcher(n_matches, mentee_id)}


@API.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    """ Returns default 500 message for many server errors.
    Mostly handles where collection is not found
    Prints the stringed exception. """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "data": {"error": str(exc)},
            "message": "server error",
        },
    )
