import sys
from fastapi.testclient import TestClient
from app.data import MongoDB
from app.api import API


class TestingPlatform():
    sys.tracebacklimit = 0
    client = TestClient(API)
    API.db = MongoDB("UnderdogDevs")

    def test_version(self):
        """ Tests the current version of the API. """

        response = self.client.get("/version")

        assert response.status_code == 200, \
            "Expected Code 200. Got " + str(response.status_code)

        assert response.json() == {'result': '0.43.7'}, \
            "Expected {'result': '0.43.7'} got " + str(response.json())

    def test_read(self):
        """ Tests whether or not a collection can be read in"""

        response = self.client.post(
            "/Mentees/read", json={'first_name': 'Sage'})

        assert response.status_code == 200, \
            "Expected Code 200. Got " + str(response.status_code)
    
    def test_collections(self):
        """ Tests collection name and size of each collection. """

        response = self.client.get("/collections")

        assert response.status_code == 200, \
            "Expected Code 200. Got " + str(response.status_code)

        assert response.json() != {}, \
            "Expected non empty JSON. Got " + str(response.json())

    def test_create_delete(self):
        """ Creates a new record.
        Input Example:
        collection = "Mentees"
        data = {
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
        }

        And checks if collection gets Deleted 
    """

        response = self.client.get("/test/create/")

        assert response.status_code == 200, \
            "Expected Code 200. Got " + str(response.status_code)
    
    def test_update(self):
        """ Returns an array containing the query and updated data. """

        profile_id = 'oW2N3A218zp83Q0i'
        response = self.client.post("/Mentees/update", json={"query": {"profile_id": profile_id},
            "update_data": {"first_name": "John"}})

        read_mentees = self.client.post(
            "/Mentees/read", json={'profile_id': profile_id})

        assert read_mentees.json()['result'][0]['first_name'] == response.json()[
            'result'][1]['first_name']

        assert read_mentees.json()['result'][0]['first_name'] == 'John'
    
    def test_search(self):
        """ Returns array of records that loosely match the search,
        automatically ordered by relevance. """

        response = self.client.post("/Mentees/search?search=Python")

        assert response.json()['result'][0]['subject'] == "Data Science: Python",\
            'Expected Data Science: Python.  Got ' + str(response.json()['result'][0]['subject'])

    def test_match(self, mentee_id: int, n_matches: int):
        """ Returns array of mentor matches for any given mentee_id. """

        profile_id = '1V165ASl8IXH7M54'

        response = self.client.post(f"/match/{profile_id}?n_matches=5")
        '''find mentor info by id of one of the mentors matches'''

        mentors_id = response.json()['result'][0]
        read_mentors = self.client.post(
            "/Mentors/read", json={'profile_id': mentors_id})

        read_mentees = self.client.post(
            "/Mentees/read", json={'profile_id': profile_id})

        '''check if their subjects indeed match'''
        assert read_mentors.json()['result'][0]['subject'] == read_mentees.json()[
            'result'][0]['subject'],\
            'Expected subjects to match got ' + str(read_mentors.json()['result'][0]['subject'])\
            + ' : ' + str(read_mentees.json()['result'][0]['subject']) 

    def test_create_delete(self, collection: str):
        """ Creates and Deletes collection  """

        response = self.client.post("/Mentees/create", data='''{
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
        response = self.client.delete("/Mentees/delete/test001")
        read = self.client.post("/Mentees/read", json={'profile_id': 'test001'})
        assert read.json()['result'] == [], 'Profile_id was not deteted'


    def test_all(self):
        """Tests all api endpoints"""
        self.test_version()
        self.test_read()
        self.test_collections()
        self.test_create_delete()
        self.test_update()
        self.test_collection_search()
        self.test_match()
        self.test_delete()


if __name__ == '__main__':
    test_api = TestingPlatform()
    test_api.test_version()
