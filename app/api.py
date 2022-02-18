from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.model import MatcherSortSearch

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.43.4",
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
    """Returns the current version of the API."""
    return {"result": API.version}


@API.get("/collections")
async def collections():
    """Returns collection names and a count of their child nodes."""
    return {"result": API.db.scan_collections()}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """Creates a new record in collection given within URL.
    
    Creates new document within given collection using the data
    parameter to populate its fields.
    
    Args:
        collection (str): Name of collection retrieved from URL
        data (dict): Key value pairs to be mapped to document fields
    
    Returns:
        New collection's data as dictionary
    """
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """Returns array of records that exactly match the query.
    
    Defines collection from URL and queries it with optional filters
    given (data). If no filtering data is given, will return all
    documents within collection.
    
    Args:
        collection (str): Name of collection retrieved from URL
        data (dict) (optional): Key value pairs to match
    
    Returns:
        List of all matching documents
    """
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """Updates collection and returns number of updated documents.
    
    Defines collection from URL and queries it with filters
    given (query). Then updates fields using update_data, either adding
    or overwriting data.
    
    Args:
        collection (str): Name of collection retrieved from URL
        query (dict): Key value pairs to filter for
        update_data (dict): Key value pairs to update
    
    Returns:
        Integer count of updated documents
    """
    return {"result": API.db.update(collection, query, update_data)}


@API.post("/{collection}/search")
async def search(collection: str, user_search: str):
    """Returns list of docs loosely matching string, sorted by relevance.
    
    Searches collection given in URL for documents that approximate the
    given string (user_search), and then presents them, automatically
    ordering results by relevance to the search.
    
    Args:
        collection (str): Name of collection to query
        user_search (str): Querying parameter
    
    Returns:
        """
    return {"result": API.db.search(collection, user_search)}


@API.post("/match/{mentee_id}")
async def match(mentee_id: int, n_matches: int):
    """Returns array of mentor matches for any given mentee_id.
    
    Utilizes imported MatcherSortSearch() to query database for the
    given number of mentors that may be a good match for the given
    mentee. See documentation for MatcherSortSearch() for details.
    
    Args:
        mentee_id (int): ID number for mentee needing a mentor
        n_matches (int): Maximum desired matching candidates
        
    Returns:
        List of mentor IDs
    """
    return {"result": API.matcher(n_matches, mentee_id)}
