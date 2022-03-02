import json
from os import getenv
from typing import Optional, List, Dict, Iterator, Tuple

from pymongo import MongoClient
from dotenv import load_dotenv
import certifi


class MongoDB:
    """Class with pymongo CRUD operations as methods
    
    This class organizes all CRUD operations into a single nexus.
    Detailed descriptions are given in individual method documentation,
    but a brief overview is given below.
    
    Args:
        database (str): Name of the database to be accessed
        
    Internal Methods:
        _connect: Connects to a given collection within the database.
    
    External Methods:
        create: Insert a document into a given collection.
        create_many: Insert many documents into a given collection.
        first: Return the first document in a given collection.
        read: Query collections and return results as a list.
        update: Updates queried document(s) in a given collection.
        delete: Deletes queried document(s) in given collection.
        count: Return count of queried documents.
        backup: Create backup JSON for given collection.
        create_index: Create given index in given collection.
        drop_index: Remove given index from given collection.
        search: Loosely search given collection with given parameters.
        scan_collections: Return all collections with document counts.
        reset_collection: Remove all documents from collection.
        """
    load_dotenv()

    def __init__(self, database: str):
        """Initializes the MongoDB class.
        
        The database parameter is taken in to identify the specific
        database within the cluster to connect to.
        
        Args:
            database (str): Name of database to connect to
        """
        self.database = database
    
    def get_database(self):
        """Connect to the database passed to the class."""
            return MongoClient(
                getenv("MONGO_URL"),
                tlsCAFile=certifi.where(),
            )[self.database]

    def get_collection(self, collection):
        """Access a collection within the predefined database."""
        return self.get_database()[collection]

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
        self.get_collection(collection).insert_one(dict(data))
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
        self.get_collection(collection).insert_many(map(dict, data))

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
        return self.get_collection(collection).find_one(query, {"_id": False})

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
       return list(self.get_collection(collection).find(query, {"_id": False}))

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
        self.get_collection(collection).update_many(query, {"$set": update_data})
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
        self.get_collection(collection).delete_many(query)

    def count(self, collection: str, query: Optional[Dict] = None) -> int:
        """Counts documents in collection that matches query.
        
        Args:
            collection (str): Name of collection to query
            query (dict): Filter query to define documents to count
        
        Returns:
            Integer count of matching documents
        """
        return self.get_collection(collection).count_documents(query or {})

    def backup(self, collection: str):
        """Create backup JSON for given collection."""
        with open("data.json", "w") as file:
            json.dump(self.read(collection), file)

    def create_index(self, collection: str):
        """Only run once - internal only!
        
        Creates an index within the given collection. This should not be
        user facing in any degree without extreme caution.
        
        Args:
            collection (str): The collection to affect
            
        Returns:
            None
        """
        self.get_collection(collection).create_index([("$**", "text")])

    def drop_index(self, collection: str):
        """Internal only!
        
        Removes existing index from the given collection. This should not
        be user facing in any degree without extreme caution.
        
        Args:
            collection (str): The collection to affect
        Returns:
            None
        """
        self.get_collection(collection).drop_index([("$**", "text")])

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

    def get_database_info(self):
        """Return dictionary of collection names and their doc counts.
        
        Uses previously established database and scans it for all
        collections, iteratively retrieving counts of documents within
        each respective collection.
        
        Args:
            None
        Returns:
            Dictionary: keys are collections, values are doc counts.
        """
        return {
            collection: self.count(collection)
            for collection in self.get_database().list_collection_names()
        }

    def reset_collection(self, collection: str):
        """Delete given collection and recreates it without documents.
        
        Resets the given collection by entirely deleting it from the
        database, and then recreating the collection without inserting
        any documents. All documents removed from this process will be
        lost entirely. Use with caution.
        
        Args:
            collection (str): The collection to reset
        Returns:
            None
        """
        self.delete(collection, {})
        self.drop_index(collection)
        self.create_index(collection)

    def make_field_unique(self, collection: str, field: str):
        self.get_collection(collection).create_index([(field, 1)], unique=True)
