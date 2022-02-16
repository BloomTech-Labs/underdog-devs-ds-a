"""
Labs DS Data Engineer Role
- Database Interface
- Visualization Interface


What to store in MongoDB?
- Admin Notes
- Survey Data
"""
import json
from os import getenv
from typing import Optional, List, Dict

from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

class MongoDB:
    """ CRUD """
    load_dotenv()

    def __init__(self, cluster: str):
        self.cluster = cluster

    def _connect(self) -> MongoClient:
        return MongoClient(getenv("MONGO_URL"))[self.cluster]

    def create(self, collection: str, data: Dict) -> Dict:
        self._connect()[collection].insert_one(dict(data))
        return data

    def read(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        return list(self._connect()[collection].find(query, {"_id": False}))

    def update(self, collection: str, query: Dict, update_data: Dict) -> int:
        n_changed_records = self.count(collection, query)
        self._connect()[collection].update_many(query, {"$set": update_data})
        return n_changed_records

    def delete(self, collection: str, query: Dict):
        self._connect()[collection].delete_many(query)

    def count(self, collection: str, query: Dict) -> int:
        return self._connect()[collection].count_documents(query)

    def backup(self, collection: str):
        with open("data.json", "w") as file:
            json.dump(self.read(collection), file)

    def create_index(self, collection: str):
        """ Only run once - internal only! """
        self._connect()[collection].create_index([("$**", "text")])

    def drop_index(self, collection: str):
        self._connect()[collection].drop_index([("$**", "text")])

    def search(self, collection: str, user_search: str) -> List[Dict]:
        return self.read(collection, {"$text": {"$search": user_search}})

    def scan_collections(self):
        return {col: self.count(col, {}) for col in self._connect().list_collection_names()}
