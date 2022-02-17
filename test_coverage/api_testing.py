import doctest
from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import API
from fastapi.testclient import TestClient

client = TestClient(API)

def test_version():
    """ Returns the current version of the API. 
        >>> client.get('/version')
        <Response [200]>
        >>> client.get('/version').json()
        {'result': '0.0.3'}
    """

def test_collections():
    """ Returns collection name and size of each collection. 
        >>> client.get('/collections')
        <Response [200]>
        >>> print(client.get('/collections').json())
    """

def test_create_read_delete(collection: str, data: Dict):
    """ Creates a new record.
        >>> client.post('/test/create', json={'john': 'doe'})
        {'result': [{'john': 'doe'}]}
        >>> client.post('/test/read').json()
        {'result': [{'john': 'doe'}]}
        >>> client.post('test/delete')
        <Response [200]>
    """

# def test_update(collection: str, query: Dict, update_data: Dict):
#     """ Returns an array containing the query and updated data. """

# def test_search(collection: str, user_search: str):
#     """ Returns array of records that loosely match the search,
#     automatically ordered by relevance. """

# def test_match(mentee_id: int, n_matches: int):
#     """ Returns array of mentor matches for any given mentee_id. """


if __name__ == "__main__":
    doctest.testmod(verbose=True)
