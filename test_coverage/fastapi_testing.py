from fastapi.testclient import TestClient
from app.api import API
client = TestClient(API)

URL = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com'


def test_version():
    response = client.get(f"{URL}/version")
    assert response.status_code == 200
    assert response.json() == {'result': '0.43.7'}, 'Versions do not match'


def test_collections():
    response = client.get(f"{URL}/collections")
    print(response.json())
    assert response.status_code == 200


def test_read():
    response = client.post(f"{URL}/Mentees/read", json={'first_name': 'John'})
    assert response.status_code == 200
    assert response.json()['result'][0]['first_name'] == 'John'


def test_create_delete():
    response = client.post(f"{URL}/Mentees/create", data='''{
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

    assert response.json()['result']['profile_id'] == 'test001'
    response = client.delete(f"{URL}/Mentees/delete/test001")
    read = client.post(f"{URL}/Mentees/read", json={'profile_id': 'test001'})
    assert read.json()['result'] == [], 'Profile_id was not deteted'


def test_search():
    response = client.post(f"{URL}/Mentees/search?search=Python")
    assert response.json()['result'][0]['subject'] == "Data Science: Python"


def test_update():
    profile_id = 'oW2N3A218zp83Q0i'
    response = client.post(f"{URL}/Mentees/update",
                           json={"query": {"profile_id": profile_id},
                                 "update_data": {"first_name": "John"}})
    read_mentees = client.post(
        f"{URL}/Mentees/read", json={'profile_id': profile_id})
    assert read_mentees.json()['result'][0]['first_name'] == response.json()[
        'result'][1]['first_name']
    assert read_mentees.json()['result'][0]['first_name'] == 'John'


def test_match():
    '''get 5 mentor matches for mentee'''
    profile_id = '1V165ASl8IXH7M54'
    response = client.post(f"{URL}/match/{profile_id}?n_matches=5")
    '''find mentor info by id of one of the mentors matches'''
    mentors_id = response.json()['result'][0]
    read_mentors = client.post(
        f"{URL}/Mentors/read", json={'profile_id': mentors_id})
    read_mentees = client.post(
        f"{URL}/Mentees/read", json={'profile_id': profile_id})
    '''check if their subjects indeed match'''
    assert read_mentors.json()['result'][0]['subject'] == read_mentees.json()[
        'result'][0]['subject']


if __name__ == '__main__':
    test_version()
    test_collections()
    test_read()
    test_create_delete()
    test_search()
    test_match()
    test_update()
    test_collections()
