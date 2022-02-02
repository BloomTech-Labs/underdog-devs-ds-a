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


@API.post("/create")
async def create(collection_name: str, data: dict):
    """ Creates a new record """
    return {"result": API.db.create(collection_name, data)}


@API.post("/read")
async def read(collection_name: str, data: dict):
    """ Returns records based on query """
    return {"result": API.db.read(collection_name, data)}


@API.post("/update")
async def update(collection_name: str, query: dict, update_data: dict):
    """ Returns the count of the updated records """
    old_data = API.db.read(collection_name, query)
    API.db.update(collection_name, query, update_data)
    new_data = API.db.read(collection_name, query)
    return {"result": "What do we return?"}


@API.post("/search")
async def search(collection_name: str, user_search: str):
    """ Returns all records that match the user_search """
    return {"result": API.db.search(collection_name, user_search)}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.api:API")
