import json
import os
from typing import Dict, Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.graphs import feedback_window, mentor_feedback_individual, mentor_feedback_dataframe
from app.model import MatcherSortSearch, MatcherSortSearchResource
from app.vader_sentiment import vader_score
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate, Feedback, FeedbackUpdate, FeedbackOptions


API = FastAPI(
    title='Underdog Devs DS API',
    version="0.48.0",
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


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """Deprecated"""
    return {"result": API.db.read(collection, data)}


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

    Example:
        /Mentees/search?search=iOS

    Args:
        collection (str): Name of collection to query
        search (str): Querying parameter

    Returns:
        List of queried documents
    """
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


@API.post("/sentiment")
async def sentiment(text: str):
    """ Returns positive, negative or neutral sentiment of the supplied text.
    Args:
        text (str): the text to be analyzed

    Returns:
        positive/negative/neutral prediction based on sentiment analysis
    """
    return {"result": vader_score(text)}


@API.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    """Read records in the feedback collection.
    Reads new document within Feedback using the ticket_id  or mentor_id parameter to
    populate its fields.
    """
    return {"result": API.db.read("Feedback", query.dict())}


@API.post("/create/feedback")
async def create_feedback(data: Feedback):
    """Create records in the feedback collection.

    Creates new document within Feedback using the Feedback schema to
    populate its fields. Creates ticket_id and vader_score automatically on submission

    Args:
        data (feedback): text, Mentor_id, mentee_id
    """
    data_dict = data.dict()
    data_dict["vader_score"] = vader_score(data_dict["text"])
    return {"result": API.db.create("Feedback", data_dict)}


@API.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    """Delete records in the feedback collection.

    Deletes document within Feedback using the ticket_id to
    populate its fields.

    Args:
        ticket_id (str): ticket_id string max length of 16
    """
    API.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}


@API.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    """Update feedback collection.

    Given a ticket_id this function updates all fields in the feedback class. Make sure to include the original
    ticket_id otherwise it will be updated with the default value. Vader_score will be updated on its own and will
    reflect the sentiment of the new text.

    Args:
        ticket_id (str): ticket ID to search by to update
        update_data (dict): Key value pairs to update

    Returns:
        result of updated data
    """
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = vader_score(data_dict["text"])
    return {"result": API.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}


@API.get("/graphs/feedback_window")
async def mentor_feedback():
    """create the dataframe for global
     mentor feedback visualization and show
     the visualization"""

    feedback_df = pd.DataFrame(API.db.read('Feedback'))
    mentee_df = pd.DataFrame(API.db.projection('Mentees', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentor_df = pd.DataFrame(API.db.projection('Mentors', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentor_feedback_df = mentor_feedback_dataframe(feedback_df, mentee_df, mentor_df)
    return json.loads(feedback_window(mentor_feedback_df).to_json())


@API.get("/graphs/mentor_feedback_individual")
async def mentor_feedback_progress():
    """create the dataframe for individual
     mentor feedback visualization and show
     visualization"""

    feedback_df = pd.DataFrame(API.db.read('Feedback'))
    mentee_df = pd.DataFrame(API.db.projection('Mentees', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentor_df = pd.DataFrame(API.db.projection('Mentors', {}, {
        "first_name": True,
        "last_name": True,
        "profile_id": True,
    }))
    mentor_feedback_df = mentor_feedback_dataframe(feedback_df, mentee_df, mentor_df)
    return json.loads(mentor_feedback_individual(mentor_feedback_df).to_json())
