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
        assert response.json() == {'result': '0.0.3'}, \
            "expected {'result': '0.0.3'} got " + str(response.json())

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
    
    def test_collection_search(self):
        """ Returns array of records that loosely match the search,
        automatically ordered by relevance. """

    def test_match(mentee_id: int, n_matches: int):
        """ Returns array of mentor matches for any given mentee_id. """

    def test_delete(collection: str):
        """ Deletes collection  """

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
