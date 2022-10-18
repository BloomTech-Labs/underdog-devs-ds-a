import unittest
from unittest.mock import patch, Mock
import pymongo.collection as collection
import pymongo.results as results
from app.data import *


class TestMongoDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_collection = "Collection"
        cls.test_entry = {"test_data": 1234}
        cls.testdb = MongoDB()
        cls.testdb.collection = Mock()
        cls.testdb.collection.return_value = collection.Collection

    @patch('pymongo.collection.Collection.insert_one')
    def test_create_success(self, mock_response):
        mock_response.return_value = results.InsertOneResult(None, acknowledged=True)
        result = self.testdb.create(self.test_collection, self.test_entry)
        self.assertTrue(result)

    @patch('pymongo.collection.Collection.insert_one')
    def test_create_failure(self, mock_response):
        mock_response.return_value = results.InsertOneResult(None, acknowledged=False)
        result = self.testdb.create(self.test_collection, self.test_entry)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
