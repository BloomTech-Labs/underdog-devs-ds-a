from fastapi.testclient import TestClient
from app.api import API

client = TestClient(API)


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


def test_read():
    response = client.post("/Mentees/read", json={'first_name': 'Sage'})
    print(response.json())
    # assert response.status_code == 200
    # assert response.json() == {'result': '0.0.3'}


if __name__ == '__main__':
    # test_version()
    # test_collections()
    test_read()
