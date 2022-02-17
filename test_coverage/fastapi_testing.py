from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB

from app.api import API

client = TestClient(API)

API.db = MongoDB("UnderdogDevs")

def test_version():
    response = client.get("/version")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'result': '0.0.3'}


def test_collections():
    response = client.get("/collections")
    print(response.json())
    # assert response.status_code == 200
    # assert response.json() == {'result': '0.0.3'}

def test_create():
    response = client.get("/test/create/")
    
    print(response.json())
    # assert response.status_code == 200


if __name__ == '__main__':
    # test_version()
    test_create()
    test_collections()
