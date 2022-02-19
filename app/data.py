import json
from os import getenv
from typing import Optional, List, Dict, Iterator, Tuple

from pymongo import MongoClient
from dotenv import load_dotenv
import certifi


class MongoDB:
    """Class with pymongo CRUD operations as methods"""
    load_dotenv()

    def __init__(self, database: str):
        """Initializes the MongoDB class.
        
        The database parameter is taken in to identify the specific
        database within the cluster to connect to.
        
        Args:
            database (str): Name of database to connect to
        """
        self.database = database

    def _connect(self, collection: str):
        """Access a given collection within the predefined database.
        
        This is used internally as a middle step for CRUD operations
        acted on specific collections.
        
        Args:
            collection (str): Name of collection to access

        Returns:
            pymongo Collection object
        """
        return MongoClient(
            getenv("MONGO_URL"),
            tlsCAFile=certifi.where()
        )[self.database][collection]

    def create(self, collection: str, data: Dict) -> Dict:
        """Insert a single document into a collection.
        
        Connects to the collection given and inserts the data as
        a single document. Data given will be mapped to dictionary
        by default.
        
        Args:
            collection (str): name of collection to add data to
            data (dict): document formatted as dictionary to be added

        Returns:
            data (dict): The data that was inserted into the collection
        """
        self._connect(collection).insert_one(dict(data))
        return data

    def create_many(self, collection: str, data: Iterator[Dict]):
        """Insert multiple documents into a collection.
        
        Connects to the collection given and inserts the data as
        a single document. Data given will be mapped to dictionary
        by default.
        
        Args:
            collection (str): name of collection to add data to
            data (dict): document formatted as dictionary to be added

        Returns:
            None
        """
        self._connect(collection).insert_many(map(dict, data))

    def first(self, collection: str, query: Optional[Dict] = None) -> Dict:
        """Return first document in collection.
        
        Returns the first document within a given collection. Optional
        filtering parameters for the query may be passed after the
        collection name.
        
        Args:
            collection (str): Name of collection to query
            query (dict) (optional): Filtering parameters
        
        Returns:
            First found document as dictionary
        """
        return self._connect(collection).find_one(query, {"_id": False})

    def read(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        """Query collection with optional parameters.
        
        Searches the given collection with the default parameter of
        _id: false and the option to include further parameters. Search
        parameters must be formatted as a dictionary.
        
        Args:
            collection (str): name of collection to query
            query (dict) (optional): List of key value pairs to match
        
        Returns:
            List of all documents matching query parameters
        """
        return list(self._connect(collection).find(query, {"_id": False}))

    def update(self, collection: str, query: Dict, update_data: Dict) -> Tuple:
        """Update existing documents in collection matching given data.
        
        Filters the given collection based on query parameters and adds
        or rewrites fields using update_data.
        
        Args:
            collection (str): Name of collection to update
            query (dict): Filter query to define documents to update
            update_data (dict): Key value pairs to update

        Returns:
            Tuple containing the filter (dict) and the update_data (dict)
        """
        self._connect(collection).update_many(query, {"$set": update_data})
        return query, update_data

    def delete(self, collection: str, query: Dict):
        """Delete existing documents in collection matching given data.
        
        Filters the given collection based on query parameters and
        deletes all matching documents.
        
        Args:
            collection (str): Name of collection to update
            query (dict): Filter query to define documents to delete

        Returns:
            None
        """
        self._connect(collection).delete_many(query)

    def count(self, collection: str, query: Optional[Dict] = None) -> int:
        """Counts documents in collection that matches query.
        
        Args:
            collection (str): Name of collection to query
            query (dict): Filter query to define documents to count
        
        Returns:
            Integer count of matching documents
        """
        return self._connect(collection).count_documents(query)

    def backup(self, collection: str):
        with open("data.json", "w") as file:
            json.dump(self.read(collection), file)

    def create_index(self, collection: str):
        """Only run once - internal only!"""
        self._connect(collection).create_index([("$**", "text")])

    def drop_index(self, collection: str):
        """Internal only"""
        self._connect(collection).drop_index([("$**", "text")])

    def search(self, collection: str, user_search: str) -> List[Dict]:
        """Loosely search given collection using given string.
        
        Performs the read method of MongoDB class, using user_search as
        a specific value parameter for query. Returns a list of matching
        documents.
        
        Args:
            collection (str): collection to query
            user_search (str): searches collection for given value
            
        Returns:
            List of matching documents
        """
        return self.read(collection, {"$text": {"$search": user_search}})

    def scan_collections(self):
        """Return dictionary of collection names and their doc counts."""
        output = {}
        cli = MongoClient(getenv("MONGO_URL"))[self.database]
        for col in cli.list_collection_names():
            output[col] = self.count(col, {})
        return output

    def reset_collection(self, collection: str):
        """Delete given collection and recreates it without documents."""
        self.delete(collection, {})
        self.drop_index(collection)
        self.create_index(collection)
