from black import json
from fastapi.testclient import TestClient
from app.api import API
import sys
client = TestClient(API)
sys.tracebacklimit = 0


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
    ''''''
    response = client.post("/Mentees/read", json={'first_name': 'Sage'})
    assert response.status_code == 200
    assert response.json()['result'][0]['first_name'] == 'Sage'


def test_create():
    response = client.post(
        '/Mentees/create', json={'profile_id': 'TEST', 'first_name': 'Jordan', 'last_name': 'Peele'})
    read = client.post('/Mentees/read', json={'first_name': 'Jordan'})
    print(response.json()['result'][0]['first_name'] == 'Jordan')


def test_delete():
    response = client.post("/Mentees/delete", json={'profile_id': 'TEST'})


if __name__ == '__main__':
    # test_version()
    # test_collections()
    test_read()
