import json
from os import getenv
from typing import Optional, List, Dict, Iterator, Tuple

from pymongo import MongoClient
from dotenv import load_dotenv
import certifi


class MongoDB:
    load_dotenv()

    def __init__(self, database: str):
        self.database = database

    def get_database(self):
        return MongoClient(
            getenv("MONGO_URL"),
            tlsCAFile=certifi.where(),
        )[self.database]

    def get_collection(self, collection):
        return self.get_database()[collection]

    def create(self, collection: str, data: Dict) -> Dict:
        self.get_collection(collection).insert_one(dict(data))
        return data

    def create_many(self, collection: str, data: Iterator[Dict]):
        self.get_collection(collection).insert_many(map(dict, data))

    def first(self, collection: str, query: Optional[Dict] = None) -> Dict:
        return self.get_collection(collection).find_one(query, {"_id": False})

    def read(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        return list(self.get_collection(collection).find(query, {"_id": False}))

    def update(self, collection: str, query: Dict, update_data: Dict) -> Tuple:
        self.get_collection(collection).update_many(query, {"$set": update_data})
        return query, update_data

    def delete(self, collection: str, query: Dict):
        self.get_collection(collection).delete_many(query)

    def count(self, collection: str, query: Optional[Dict] = None) -> int:
        return self.get_collection(collection).count_documents(query)

    def backup(self, collection: str):
        with open("data.json", "w") as file:
            json.dump(self.read(collection), file)

    def create_index(self, collection: str):
        """ Only run once - internal only! """
        self.get_collection(collection).create_index([("$**", "text")])

    def drop_index(self, collection: str):
        self.get_collection(collection).drop_index([("$**", "text")])

    def search(self, collection: str, user_search: str) -> List[Dict]:
        return self.read(collection, {"$text": {"$search": user_search}})

    def get_database_info(self):
        return {
            collection: self.count(collection)
            for collection in self.get_database().list_collection_names()
        }

    def reset_collection(self, collection: str):
        self.delete(collection, {})
        self.drop_index(collection)
        self.create_index(collection)

    def make_field_unique(self, collection: str, field: str):
        self.get_collection(collection).create_index([(field, 1)], unique=True)


if __name__ == '__main__':
    db = MongoDB("UnderdogDevs")
    db.get_collection("Mentees").drop_index([("user_id", 1)])
    db.get_collection("Mentors").drop_index([("user_id", 1)])
