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
    """API version and password
    <pre><code>
    @return: JSON[JSON[String,String]]</pre></code>"""
    local = os.getenv("CONTEXT") == "local"
    remote = "Run the API locally with the proper environment variables"
    password = API.db.first("Secret")["Password"] if local else remote
    return {"result": {"Version": API.version, "Password": password}}


@API.get("/collections")
async def collections():
    """Names of collections and the count of documents in each collection
    <pre><code>
    @return JSON[JSON[String,Integer]]</pre></code>"""
    return {"result": API.db.get_database_info()}


@API.post("/read/mentor")
async def read_mentor(data: Optional[Dict] = None):
    """Displays mentor(s) who meet provided criteria. Displays all mentors if no input provided
    <pre><code>
    @param data: JSON[Optional[Dict]]
    @return JSON[Array[Mentor]]</pre></code>"""
    return {"result": API.db.read("Mentors", data)}


@API.post("/read/mentee")
async def read_mentee(data: Optional[Dict] = None):
    """Displays mentee(s) who meet provided criteria. Displays all mentees if no input provided
    <pre><code>
    @param data: JSON[Optional[Dict]]
    @return JSON[Array[Mentee]]</pre></code>"""
    return {"result": API.db.read("Mentees", data)}


@API.post("/create/mentor")
async def create_mentor(data: Mentor):
    """Creates a mentor
    <pre><code>
    @param data: JSON[Mentor]
    @return JSON[Boolean] - Indicates success or failure of document creation</pre></code>"""
    try:
        return {"result": API.db.create("Mentors", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/create/mentee")
async def create_mentee(data: Mentee):
    """Creates a mentee
    <pre><code>
    @param data: JSON[Mentee]
    @return JSON[Boolean] - Indicates success or failure of document creation</pre></code>"""
    try:
        return {"result": API.db.create("Mentees", data.dict())}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Profile ID must be unique.")


@API.post("/update/mentor/{profile_id}")
async def update_mentors(profile_id: str, update_data: MentorUpdate):
    """Updates a mentor
    <pre><code>
    @param profile_id: str
    @param update_data: JSON[MentorUpdate]
    @return JSON[Boolean] - Indicates success or failure of update</pre></code>"""
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentors", {"profile_id": profile_id}, data)}


@API.post("/update/mentee/{profile_id}")
async def update_mentees(profile_id: str, update_data: MenteeUpdate):
    """Updates a mentee
    <pre><code>
    @param profile_id: str
    @param update_data: JSON[MenteeUpdate]
    @return JSON[Boolean] - Indicates success or failure of update</pre></code>"""
    data = update_data.dict(exclude_none=True)
    return {"result": API.db.update("Mentees", {"profile_id": profile_id}, data)}


@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """Returns n_matches mentor profiles for mentee profile_id
    <pre><code>
    @param profile_id: str
    @param n_matches: int
    @return JSON[Array[profile_id]]</pre></code>"""
    return {"result": API.matcher(n_matches, profile_id)}


@API.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    """Returns mentee feedback
    <pre><code>
    @param query: FeedbackOptions
    @return JSON[Array[Feedback]]</pre></code>"""
    return {"result": API.db.read("Feedback", query.dict(exclude_none=True))}


@API.post("/create/feedback")
async def create_feedback(data: Feedback):
    """Creates feedback (with vadersentiment analysis)
    <pre><code>
    @param data: Feedback
    @return JSON[Boolean] - Indicates success or failure of feedback creation</pre></code>"""
    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.create("Feedback", data_dict)}


@API.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    """Deletes feedback
    <pre><code>
    @param ticket_id: str
    @return JSON[JSON[ticket_id]]</pre></code>"""
    API.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}


@API.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    """Updates feedback
    <pre><code>
    @param ticket_id: str
    @param update_data: FeedbackUpdate
    @return JSON[Boolean] - indicates success or failure of update</pre></code>"""
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": API.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}


@API.get("/graph/tech-stack-by-role")
async def tech_stack_by_role():
    """Tech Stack Count by Role, stacked bar chart
    <pre><code>
    @return JSON[Altair.Chart]</pre></code>"""
    return stacked_bar_chart(
        df_tech_stack_by_role(API.db),
        "tech_stack",
        "role",
    ).to_dict()
