"""
BloomTech Labs DS Machine Learning Operations Role
- Application Programming Interface
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.0.1",
    docs_url='/',
)

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    return {"version": API.version}
