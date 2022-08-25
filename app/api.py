import os
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import DuplicateKeyError

from app.data import MongoDB
from app.graphs import stacked_bar_chart, df_tech_stack_by_role
from app.model import MatcherSortSearch
from app.sentiment import sentiment_rank
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate
from app.schema import Feedback, FeedbackUpdate, FeedbackOptions

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.49.1",
    docs_url='/',
)

API.db = MongoDB()
API.matcher = MatcherSortSearch()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.get("/version")
async def version():
    """
    API version and password (correct password returned in local setup).

    Returns
    ----------
    Result: JSON Object
        Key-value pairs for version and password.
    """

    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections")
async def collections():
    """
    Names of collections and the count of documents in each collection.

    Returns
    ----------
    Result: JSON Object
        "CollectionName"(str): "count"(int)
    """

    return {"result": API.db.get_database_info()}


@API.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
    """
    Given key-value pair Returns an array/object of mentors whose profiles meet the specified criteria,
    or if given no input Returns data for all mentors.

    Parameters
    ----------
    JSON Object
        {"KeyName":Value, "KeyName2":Value2}
            Object can contain one or more key-value pairs. For a complete list
            of possible key-value pairs, see Example Schema in /create/mento.
    Returns
    ----------
    JSON Object
        Array of mentor profile documents.

    """

    return {"result": API.db.read("Mentors", data)}


@API.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    """
    Returns an array of all mentees whose profiles meet the specified criteria.

    Parameters
    ----------
    JSON Object
        {"KeyName":Value, "KeyName2":Value2}
            Object can contain one or more key-value pairs. For a complete list
            of possible key-value pairs, see Example Schema in /create/mentee.
    Returns
    ----------
    JSON Object
        Array of mentee profile documents.
    """
    return {"result": API.db.read("Mentees", data)}


@API.post("/create/mentor")
async def create_mentor(data: Mentor):
    """
    Creates a mentor document (profile).

    Parameters
    ----------
    user: JSON Object
        See Example Value for structure and data types of key-value pairs. "referred_by" and "other_info" are optional;
        all other fields are required.
    Returns
    ----------
    success: bool
        Indicates success or failure of document creation.
    """
    try:
        return {"result": API.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/create/mentee")
async def create_mentee(data: Mentee):
    """
    Creates a mentee document (profile).

    Parameters
    ----------
    user: JSON Object
        See Example Value for structure and data types of key-value pairs. "convictions" and "other_info" are optional;
        all other fields are required.
    Returns
    ----------
    success: bool
        Indicates success or failure of document creation.
    """

    try:
        return {"result": API.db.create("Mentees", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    """
    Updates a mentor document (profile).
    Parameters
    ----------
    profile_id: string
    update_data: JSON Object
        Key-value pairs to be updated. Can accept one or more key-value pairs. See Example Value for valid key-value
        pairs.
    Returns
    ----------
    profile_id, user: array
        Returns profile_id and updated mentor document.
    """

    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentors", {"profile_id": profile_id}, data)}


@API.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    """
    Updates a mentee document (profile).

    Parameters
    ----------
    profile_id: string
    update_data: JSON Object
        Key-value pairs to be updated. Can accept one or more key-value pairs. See Example Value for valid key-value
        pairs.

    Returns
    ----------
    profile_id, user: array
        Returns profile_id and updated mentee document.
    """

    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentees", {"profile_id": profile_id}, data)}


@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """
    Returns n_matches mentor profiles for mentee profile_id.

    Parameters
    ----------
    profile_id: str
    n_matches: int

    Returns
    ----------
    profile_id : array

    """

    return {"result": API.matcher(n_matches, profile_id)}


@API.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    """
    Returns mentee feedback.

    Parameters
    ----------
    ticket_id: str
    mentee_id: str
    mentor_id: str

    Returns
    ---------
    Feedback JSON Object

    """

    return {"result": API.db.read("Feedback", query.dict(exclude_none=True))}


@API.post("/create/feedback")
async def create_feedback(data: Feedback):
    """
    Returns vadersentiment analysis for mentor and mentee feedback in the form of an array/object.

    Parameters
    ----------
    text: str
    ticket_id: str
    mentee_id: str
    mentor_id: str

    Return
    ---------
    Feedback JSON Object.
        Returns parameters and vader_score.

    """

    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.create("Feedback", data_dict)}


@API.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    """
    Deletes mentee feedback.

    Parameters
    ----------
    ticket_id: str

    Returns
    ----------
    JSON object with deletion confirmation.
    """

    API.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}


@API.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    """
    Updates mentee feedback.

    Parameters
    ----------
    ticket_id: str
    text: str
    mentee_id: str
    mentor_id: str

    Returns
    ----------
    JSON object with updated vader_score.

    """

    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}


@API.get("/graph/tech-stack-by-role")
async def tech_stack_by_role():
    """
    Tech Stack Count by Role - stacked bar chart.


    Returns
    ----------
    Altair Chart in JSON format.

    """
    return stacked_bar_chart(
        df_tech_stack_by_role(API.db),
        "tech_stack",
        "role",
    ).to_dict()
