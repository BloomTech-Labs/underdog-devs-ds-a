from typing import Collection
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
    assert response.status_code == 200


def test_read():
    ''''''
    response = client.post("/Mentees/read", json={'first_name': 'Sage'})
    assert response.status_code == 200
    assert response.json()['result'][0]['first_name'] == 'Sage'


def test_create_delete():
    response = client.post('/Mentees/create', data='''{
        "profile_id": "test001",
        "first_name": "Luca",
        "last_name": "Evans",
        "email": "fake@email.com",
        "city": "Ashland",
        "state": "Oregon",
        "country": "USA",
        "formerly_incarcerated": true,
        "underrepresented_group": true,
        "low_income": true,
        "list_convictions": [
          "Infraction",
          "Felony"
        ],
        "subject": "Web: HTML, CSS, JavaScript",
        "experience_level": "Beginner",
        "job_help": false,
        "industry_knowledge": false,
        "pair_programming": true,
        "other_info": "Notes"
    }''')

    assert response.json()['result']['profile_id'] == 'test001', 'ERROR'
    response = client.delete('/Mentees/delete/test001')
    read = client.post("/Mentees/read", json={'profile_id': 'test001'})
    assert read.json()['result'] == [], 'ERROR'


def test_search():
    response = client.post('/Mentees/search?search=Python')
    print(response.json())
    assert response.json()['result'][0]['subject'] == "Data Science: Python"


# def test_update():
#     response = client.post('/Mentees/update', query={''}, update_data=)


def test_match():
    '''get mentor matches for mentee'''
    profile_id = '1V165ASl8IXH7M54'
    response = client.post(f'/match/{profile_id}?n_matches=5')
    '''find mentor info by id of one of the mentors matches'''
    mentors_id = response.json()['result'][0]
    read_mentors = client.post(
        "/Mentors/read", json={'profile_id': mentors_id})
    read_mentors = client.post(
        "/Mentees/read", json={'profile_id': profile_id})
    '''check if their subjects'''
    assert read_mentors.json()['result'][0]['subject'] == read_mentors.json()[
        'result'][0]['subject']


if __name__ == '__main__':
    # test_version()
    # test_read()
    # test_create_delete()
    test_collections()
    # test_search()
    test_match()
