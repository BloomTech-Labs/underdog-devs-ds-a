import datetime
import json
import os
from typing import Dict, Optional

import pandas as pd
from fastapi import FastAPI, status, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from app.data import MongoDB
from app.graphs import tech_stack_by_role
from app.utilities import financial_aid_gen
from app.model import MatcherSortSearch, MatcherSortSearchResource
from app.vader_sentiment import vader_score
from app.computer_assignment import computer_assignment_visualizer
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate
from data_generators.user_generators import generate_uuid
API = FastAPI(
    title='Underdog Devs DS API',
    version="0.46.2",
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


@API.get("/version")
async def version():
    """Return the current version of the API."""
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally to get the password"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {
        "Version": API.version,
        "Password": password,
    }}


@API.get("/collections")
async def collections():
    """Return collection names and a count of their child nodes."""
    return {"result": API.db.get_database_info()}


@API.get("/cavisualizer", response_class=HTMLResponse)
async def computer_assignment_rating_visualizer():
    """Return an HTML table of the computer assignment
    ratings in the computer assignment collection of the
    selected mongodb database.
    """
    return computer_assignment_visualizer(API.db)


@API.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
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
async def read_mentee(data: Optional[Dict] = None):
    """Return array of records that exactly match the given query from Mentees.
    Queries from Mentees collection with optional filters given (data).
    If no filtering data is given, will return all documents within collection.
    Args:
        data (dict) (optional): Key value pairs to match
    Returns: List of all matching documents in the Mentees collection
    """
    return {"result": API.db.read("Mentees", data)}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """Create a new record in the given collection.

    Creates new document within given collection using the data
    parameter to populate its fields.

    Args:
        collection (str): Name of collection retrieved from URL
        data (dict): Key value pairs to be mapped to document fields

        Input Example:
        collection = "Mentees"

    Returns:
        New collection's data as dictionary
    """
    await is_collection(collection)
    return {"result": API.db.create(collection, data)}


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


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """Update collection and return the number of updated documents.

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
    await is_collection(collection)
    return {"result": API.db.update(collection, query, update_data)}


@API.post("/create/mentor")
async def create_mentor(data: Mentor):
    """Create a new record in the Mentors collection.

    Creates new document within Mentors using the data parameter to
    populate its fields. This also uses Pydantic schema to validate
    incoming data follows the rules.

    Args:
        data (Mentor): Mentor
    Returns:
        New record data or schema discrepancy error as dictionary
    """
    return {"result": API.db.create("Mentors", data.dict())}


@API.post("/create/mentee")
async def create_mentee(data: Mentee):
    """Create a new record in the Mentees collection.

    Creates new document within Mentees using the data parameter to
    populate its fields. This also uses Pydantic schema to validate
    incoming data follows the rules.

    Args:
        data (Mentee): Mentee
    Returns:
        New record data or schema discrepancy error as dictionary
    """
    return {"result": API.db.create("Mentees", data.dict())}


@API.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    """Updates Mentor document.
    Validate changes in update_data using MentorUpdate class (Pydantic schema)
    and updates the corresponding fields, by overwriting or adding data.
    Args:
        profile_id (str): User Id
        update_data (dict): Key value pairs to update
    Returns:
        Updated fields or schema discrepancy error as dictionary
    """
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentors", {"profile_id": profile_id}, data)}


@API.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    """Updates Mentee document.
    Validate changes in update_data using MenteeUpdate class (Pydantic schema)
    and updates the corresponding fields, by overwriting or adding data.
    Args:
        profile_id (str): User Id
        update_data (dict): Key value pairs to update
    Returns:
        Updated fields or schema discrepancy error as dictionary
    """
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentees", {"profile_id": profile_id}, data)}


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


@API.post("/match_resource/{item_id}")
async def match_resource(item_id: str, n_matches: int):
    """ Returns array of mentee matches for any given Resource item_id.

    Utilizes imported MatcherSortSearchResource() to query database for the
    given number of mentees that may be a good match for the given
    Resource(s). See documentation for MatcherSortSearchResource() for details.

    Args:
        item_id (int): ID number for resource item to be allocated to a mentee
        n_matches (int): Maximum desired matching candidates.

    Returns:
        List of mentee ID(s) """
    return {"result": API.resource_matcher(n_matches, item_id)}


@API.delete("/{collection}/delete/{profile_id}")
async def delete(collection: str, profile_id: str):
    """Removes a user from the given collection.
    Deletes all documents containing the given profile_id permanently,
    and returns the deleted profile_id for confirmation.
    Args:
        collection (str): Name of collection to query for deletion
        profile_id (str): ID number of user to be deleted
    Returns:
        Dictionary with key of "deleted" and value of the profile_id
    """
    await is_collection(collection)
    API.db.delete(collection, {"profile_id": profile_id})
    return {"result": {"deleted": profile_id}}


@API.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    """Returns default 500 message for many server errors.
    Mostly handles where collection is not found
    Prints the stringed exception."""

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "data": {"error": str(exc)},
            "message": "server error",
        },
    )


@API.post("/financial_aid/{profile_id}")
async def financial_aid(profile_id: str):
    """Returns the probability that financial aid will be required.

    Calls the financial aid function from functions.py imputing the
    profile_id for calculation involving formally incarcerated, low income,
    and experience level as variables to formulate probability of financial aid

    Args:
        profile_id (str): the profile id of the mentee

    Returns:
        the probability that financial aid will be required
    """

    profile = API.db.first('Mentees', {"profile_id": profile_id})

    if not profile:
        raise HTTPException(status_code=404, detail="Mentee not found")

    return {"result": financial_aid_gen(profile)}


@API.post("/sentiment")
async def sentiment(text: str):
    """ Returns positive, negative or neutral sentiment of the supplied text.
    Args:
        text (str): the text to be analyzed

    Returns:
        positive/negative/neutral prediction based on sentiment analysis
    """
    return {"result": vader_score(text)}


@API.get("/graphs/tech-stack-by-role")
async def tech_stack_graph():
    mentors_df = pd.DataFrame(API.db.read("Mentors"))[["tech_stack", "name"]]
    mentees_df = pd.DataFrame(API.db.read("Mentees"))[["tech_stack", "name"]]
    mentors_df["user_role"] = "Mentor"
    mentees_df["user_role"] = "Mentee"
    df = pd.concat([mentees_df, mentors_df], axis=0).reset_index(drop=True)
    return json.loads(tech_stack_by_role(df).to_json())


@API.post("/query/Feedback")
async def feedback_crud(crud: str, mentee_id: Optional[str] = None, mentor_id: Optional[str] = None,
                        feedback: Optional[str] = None, ticket_id: Optional[str] = None):
    """Create, read, update and delete records in the feedback collection.

    Creates new document within Feedback using the data parameter to
    populate its fields.

    Args:
    - crud (create, read and delete): choice (pick 1)
    - ticket_id (uuid) : autogenerated 16 digit ID (optional)
    - mentee_id (str): Mentee ID (optional)
    - mentor_id (str): Mentor ID (optional)
    - feedback (str): feedback (optional)
    - date_time (datetime): current datetime
    - vader_score(str): compound sentiment value

    Returns:
    - if crud == create -> supply mentee_id, mentor_id and feedback
    - if crud == read -> supply ticket_id or mentor_id to view specific ticket or None to view all tickets
    - if crud == delete -> supply ticket_id to delete ticket
    """

    if crud == 'create' and (mentee_id, mentor_id, feedback):
        feedback_score = vader_score(feedback)
        return {"result": API.db.create("Feedback", {"ticket_id": generate_uuid(16),
                                                     'mentee_id': mentee_id, 'mentor_id': mentor_id,
                                                     'feedback': feedback, 'datetime': datetime.datetime.now(),
                                                     'vader_score': feedback_score})}

    elif crud == 'read':
        if ticket_id:
            return {"result": API.db.read("Feedback", {'ticket_id': ticket_id})}
        else:
            return {"result": API.db.read("Feedback", ticket_id)}

    elif crud == 'delete':
        API.db.delete("Feedback", {"ticket_id": ticket_id})
        return {"result": {"deleted": ticket_id}}

    else:
        return 'Modify_option needs to be create, read or delete'
