import sys
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from app.data import MongoDB

from app.api import API

class TestingPlatform():
    sys.tracebacklimit = 0
    client = TestClient(API)
    API.db = MongoDB("UnderdogDevs")

    def test_version(self):
        response = self.client.get("/version")
        assert response.status_code == 200
        assert response.json() == {'result': '0.0.3'}, \
            "expected {'result': '0.0.3'} got " + str(response.json())


    def test_collections(self):
        response = self.client.get("/collections")
        print(response.json())
        assert response.status_code == 200
        #we could test more than that if need be?

    def test_create_read_delete(self):
        response = self.client.get("/test/create/")
        
        print(response.json())
        # assert response.status_code == 200


if __name__ == '__main__':
    test_api = TestingPlatform()
    test_api.test_version()
