from cgi import test
import json
import sys
from fastapi.testclient import TestClient
from app.api import API
from data_generators.user_generators import Mentee, Mentor
from pprint import pprint


class TestingPlatform():
    sys.tracebacklimit = 0
    client = TestClient(API)
    repopulate = False
    def test_version(self):
        """ Tests the current version of the API. """

        response = self.client.get("/version")

        assert response.status_code == 200, \
            pprint("test_version: Expected Code 200. Got " +
                   str(response.status_code))

        assert response.json() == {'result': '0.43.7'}, \
            pprint("test_version: Expected 0.43.7. Got " + str(response.json()))

    def test_read(self, query=None):
        """ Tests whether or not a collection can be read in"""

        response = self.client.post(
            "/Mentees/read", json=query or None)

        assert response.status_code == 200, \
            pprint("test_read: Expected Code 200. Got " +
                   str(response.status_code))

        assert response.json() != {}, \
            pprint("test_read: Expected non empty json. Got " +
                   str(response.json()))

    def test_collections(self):
        """ Tests collection name and size of each collection. """

        response = self.client.get("/collections")

        assert response.status_code == 200, \
            pprint("test_collections: Expected Code 200. Got " +
                   str(response.status_code))

        assert response.json() != {}, \
            "test_collections: Expected non empty JSON. Got " + \
            str(response.json())

    def test_update(self, query):
        # Run after create
        """ Returns an array containing the query and updated data. """
        update = self.client.post("/Mentees/update",
                                  json={"query": {"profile_id": "test001"},
                                        "update_data": {"city": "Glorious", "state": "Homeland"}})
        read = self.client.post(
            "/Mentees/read", json={"profile_id": "test001"})

        assert update.json() == read.json(), "test_update: Expected the update to equal " + str(read.json()) \
            + ". Got " + str(update.json())

    def test_search(self, query):
        """ Returns array of records that loosely match the search,
        automatically ordered by relevance. """

        response = self.client.post("/Mentees/search?search=Python")

        assert response.json()['result'][0]['subject'] == "Data Science: Python",\
            'test_search: Expected Data Science: Python. Got ' + \
            str(response.json()['result'][0]['subject'])

    def test_match(self, mentee_id: int, n_matches: int):
        """ Returns array of mentor matches for any given mentee_id. """

        profile_id = '1V165ASl8IXH7M54'

        response = self.client.post(f"/match/{profile_id}?n_matches=5")
        '''find mentor info by id of one of the mentors matches'''

        mentors_id = response.json()['result'][0]
        read_mentors = self.client.post(
            "/Mentors/read", json={'profile_id': mentors_id})

        read_mentees = self.client.post(
            "/Mentors/read", json={'profile_id': mentee_id})

        '''check if their subjects indeed match'''

        assert read_mentors.json()['result'][0]['subject'] == read_mentees.json()[
            'result'][0]['subject'],\
            'test_match: Expected subjects to match got ' + str(read_mentors.json()['result'][0]['subject'])\
            + ' : ' + str(read_mentees.json()['result'][0]['subject'])

    def test_create(self):
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

        read = self.client.post(
            "Mentees/read", json={'profile_id': 'test001'})
        assert read.json()['result'][0] == response.json()['result'], pprint(
            f"test_create: Expected {str(response.json())}.\n\nGot " + str(read.json()))

    def test_delete(self):
        """ Deletes mentor/mentee in a collection"""
        response = self.client.delete("/Mentees/delete/test001")

    def test_integration(self):
        """Tests all api endpoints"""
        self.test_read()

        # if read works then we can use it as the basis for the rest.
        self.test_create()
        self.test_update()

        self.test_delete()

    def populate_db(self):
        API.db.reset_collection("Mentees")
        API.db.make_field_unique("Mentees", "profile_id")
        API.db.create_many("Mentees", (vars(Mentee()) for _ in range(100)))
        API.db.reset_collection("Mentors")
        API.db.make_field_unique("Mentors", "profile_id")
        API.db.create_many("Mentors", (vars(Mentor()) for _ in range(20)))

if __name__ == '__main__':
    test_api = TestingPlatform()
    
    if test_api.repopulate:
        test_api.populate_db()
    
    test_api.test_version()
    test_api.test_collections()

    test_api.test_integration()
