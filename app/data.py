from datetime import datetime
import json
from os import getenv
from typing import Optional, List, Dict, Iterator, Tuple

from pymongo import MongoClient
from dotenv import load_dotenv


class MongoDB:
    load_dotenv()

    def database(self):
        return MongoClient(getenv("MONGO_URL"))["UnderdogDevs"]

    def collection(self, collection):
        return self.database()[collection]

    def create(self, collection: str, data: Dict) -> bool:
        """ Insert a single document into a collection """
        return self.collection(
            collection,
        ).insert_one(self.timestamp(data)).acknowledged

    def create_many(self, collection: str, data: Iterator[Dict]):
        """ Insert multiple documents into a collection """
        self.collection(collection).insert_many(map(dict, data))

    def first(self, collection: str, query: Optional[Dict] = None) -> Dict:
        """ Return first document in collection """
        return self.collection(collection).find_one(query, {"_id": False})

    def read(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        """ Query collection with optional parameters """
        return list(self.collection(collection).find(query, {"_id": False}))

    def projection(self, collection: str, query: Dict, projection: Dict) -> List[Dict]:
        """ Query collection with specific parameters """
        projection["_id"] = False
        return list(self.collection(collection).find(query, projection))

    def update(self, collection: str, query: Dict, update_data: Dict) -> Tuple:
        """ Update existing documents in collection matching given data """
        self.collection(collection).update_many(
            query, {"$set": self.timestamp(update_data, "updated_at")}
        )
        return query, update_data

    def delete(self, collection: str, query: Dict):
        """ Delete existing documents in collection matching given data """
        self.collection(collection).delete_many(query)

    def count(self, collection: str, query: Optional[Dict]) -> int:
        """ Returns the number of documents in collection that matches query """
        return self.collection(collection).count_documents(query or {})

    def backup(self, collection: str):
        """Create backup JSON for given collection."""
        with open("data.json", "w") as file:
            json.dump(self.read(collection), file)

    def create_index(self, collection: str):
        """ Internal only! Creates an index within the given collection. """
        self.collection(collection).create_index([("$**", "text")])

    def drop_index(self, collection: str):
        """ Internal only! Removes existing index from the given collection """
        self.collection(collection).drop_index([("$**", "text")])

    def search(self, collection: str, user_search: str) -> List[Dict]:
        """ Loosely search given collection using given string """
        return self.read(collection, {"$text": {"$search": user_search}})

    def get_database_info(self):
        """ Returns all collection names and their doc counts """
        return {
            collection: self.count(collection)
            for collection in self.database().list_collection_names()
        }

    def reset_collection(self, collection: str):
        """ Deletes all records in a given collection and resets the index """
        self.delete(collection, {})
        self.drop_index(collection)
        self.create_index(collection)

    def make_field_unique(self, collection: str, field: str):
        """ Makes a given field in a given collection unique """
        self.collection(collection).create_index([(field, 1)], unique=True)

    @staticmethod
    def timestamp(data: Dict, label: str = "created_at") -> Dict:
        """ Generates a timestamp and applies it to a record """
        data[label] = datetime.now()
        return data
