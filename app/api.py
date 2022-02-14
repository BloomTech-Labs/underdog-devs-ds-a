"""
BloomTech Labs DS Machine Learning Operations Role
- Application Programming Interface

- Project: UnderdogDevs
- Cluster:
- Databases:
    - Mentee
        - Mentee Application
        - Mentee Exit Survey (When Mentees graduate)
    - Mentor
        - Mentor Application
        - Mentor Exit Survey (When Mentees graduate)
        - Mentor Notes
    - Admin
        - Admin Notes
"""
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB


API = FastAPI(
    title='Underdog Devs DS API',
    version="0.0.2",
    docs_url='/',
)

API.db = MongoDB("UnderdogDevs")

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    return {"result": API.version}


@API.get("/scan_collections")
async def scan_collections():
    """ Self scans and returns names of collections along with thier size """
    return {"result": API.db.scan_collections()}


@API.post("/create")
async def create(collection_name: str, data: Dict):
    """ Creates a new record """
    return {"result": API.db.create(collection_name, data)}


@API.post("/read")
async def read(collection_name: str, data: Dict):
    """ Returns records based on query """
    return {"result": API.db.read(collection_name, data)}


@API.post("/update")
async def update(collection_name: str, query: Dict, update_data: Dict):
    """ Returns the count of the updated records """
    API.db.update(collection_name, query, update_data)
    return {"result": (query, update_data)}


@API.post("/search")
async def search(collection_name: str, user_search: str):
    """ Returns all records that match the user_search """
    return {"result": API.db.search(collection_name, user_search)}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.api:API")
