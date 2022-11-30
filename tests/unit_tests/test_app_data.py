from datetime import datetime
import time
import unittest
from unittest.mock import Mock, patch

import pymongo.collection as collection
import pymongo.results as results

from app.data import MongoDB


class TestMongoDBQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize environment for test suite."""
        cls.test_collection = "Test_Collection"
        cls.test_entry = {"test": "something"}
        cls.test_doc_id = "test_id"

        MongoDB.collection = Mock()
        MongoDB.collection.return_value = collection.Collection

    def setUp(self):
        """Initialize object(s) before each test case."""
        self.test_db = MongoDB()

    @patch('pymongo.collection.Collection.insert_one')
    def test_create_response(self, mock_response):
        mock_response.return_value = results.InsertOneResult(
            self.test_doc_id, acknowledged=True)
        response = self.test_db.create(self.test_collection, self.test_entry)
        self.assertTrue(response)
        mock_response.return_value = results.InsertOneResult(
            self.test_doc_id, acknowledged=False)
        response = self.test_db.create(self.test_collection, self.test_entry)
        self.assertFalse(response)

    @patch('pymongo.collection.Collection.update_many')
    def test_update_response(self, mock_response):
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=True)
        response = self.test_db.update(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertTrue(response)
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=False)
        response = self.test_db.update(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertFalse(response)

    @patch('pymongo.collection.Collection.update_one')
    def test_delete_from_array_response(self, mock_response):
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=True)
        response = self.test_db.delete_from_array(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertTrue(response)
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=False)
        response = self.test_db.delete_from_array(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertFalse(response)

    @patch('pymongo.collection.Collection.update_one')
    def test_upsert_to_set_array_response(self, mock_response):
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=True)
        response = self.test_db.upsert_to_set_array(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertTrue(response)
        mock_response.return_value = results.UpdateResult(
            self.test_doc_id, acknowledged=False)
        response = self.test_db.upsert_to_set_array(
            self.test_collection, self.test_entry, self.test_entry)
        self.assertFalse(response)


class TestMongoDBTimestamp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize environment for test suite."""
        cls.test_entry = {"test": "something"}

    def setUp(self):
        """Initialize object(s) before each test case."""
        self.test_db = MongoDB()

    def test_timestamp_default(self):
        result = self.test_db.timestamp(self.test_entry)
        self.assertIn("created_at", result.keys())
        self.assertIsInstance(result["created_at"], datetime)

    def test_timestamp_label(self):
        result = self.test_db.timestamp(self.test_entry, "test_timestamp")
        self.assertIn("test_timestamp", result.keys())

    def test_timestamp_time(self):
        result = self.test_db.timestamp({})
        self.assertAlmostEqual(
            result["created_at"].timestamp(), time.time(), 4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
