import json
from typing import Dict, Optional
import pandas as pd
from fastapi import FastAPI, status, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.data import MongoDB
from app.model import MatcherSortSearch, MatcherSortSearchResource
from app.computer_assignment import computer_assignment_visualizer
from app.schema import Mentee, MenteeUpdate, Mentor, MentorUpdate

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.45.3",
    docs_url='/',
)
API.db = MongoDB("UnderdogDevs")
API.matcher = MatcherSortSearch()
API.resource_matcher = MatcherSortSearchResource()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def is_collection(collection: str):
    known_collections = (await collections()).get("result").keys()
    if collection not in known_collections:
        raise HTTPException(
            status_code=404,
            detail=f"Collection: '{collection}', not found",
        )


@API.get("/cavisualizer", response_class=HTMLResponse)
async def computer_assignment_rating_visualizer():
    """Return an HTML table of the computer assignment
    ratings in the computer assignment collection of the
    selected mongodb database.
    """
    return computer_assignment_visualizer(API.db)


@API.post("/read/mentor")
async def read(data: Optional[Dict] = None):
    """Return array of records that exactly match the given query from Mentors.
    Queries from Mentors collection with optional filters
    given (data). If no filtering data is given, will return all
    documents within Mentors collection.
    Args:
        data (dict) (optional): Key value pairs to match
    Returns: List of all matching documents in the Mentors collection
    """
    return {"result": API.db.read("Mentors", data)}


@API.post("/read/mentee")
async def read(data: Optional[Dict] = None):
    """Return array of records that exactly match the given query from Mentees.
    Queries from Mentees collection with optional filters given (data).
    If no filtering data is given, will return all documents within collection.
    Args:
        data (dict) (optional): Key value pairs to match
    Returns: List of all matching documents
    """
    return {"result": API.db.read("Mentees", data)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """Return array of records that exactly match the given query.
    Defines collection from URL and queries it with optional filters
    given (data). If no filtering data is given, will return all
    documents within collection.
    Args:
        collection (str): Name of collection retrieved from URL
        data (dict) (optional): Key value pairs to match
    Returns:
        List of all matching documents
    """
    await is_collection(collection)
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/search")
async def collection_search(collection: str, search: str):
    """Return list of docs loosely matching string, sorted by relevance.
    Searches collection given in URL for documents that approximate the
    given string (search), and then presents them, automatically
    ordering results by relevance to the search.
    Args:
        collection (str): Name of collection to query
        search (str): Querying parameter
    Returns:
        List of queried documents
    """
    await is_collection(collection)
    return {"result": API.db.search(collection, search)}


@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """Return an array of mentor matches for any given mentee profile_id.
    Utilizes imported MatcherSortSearch() to query database for the
    given number of mentors that may be a good match for the given
    mentee. See documentation for MatcherSortSearch() for details.
    Args:
        profile_id (str): ID number for mentee needing a mentor
        n_matches (int): Maximum desired matching candidates
    Returns:
        List of mentor IDs
    """
    return {"result": API.matcher(n_matches, profile_id)}
