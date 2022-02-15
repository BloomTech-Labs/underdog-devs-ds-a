import requests
import doctest
from app.api import version, scan_collections, create, read, update, search
from app.api import API


link=''
requests.get('link')


def test_coverage(version, scan_collections, create, read, update, search):
    version({"result": API.version})

    scan_collections({"result": API.db.scan_collections()})
    """ Self scans and returns names of collections along with thier size """

    create({"result": API.db.create(collection_name, data)})
    """ Creates a new record 
        (collection_name: str, data: Dict)"""

    read({"result": API.db.read(collection_name, data)})
    """ Returns records based on query
        (collection_name: str, data: Dict)"""

    update(collection_name: str, query: Dict, update_data: Dict):
    """ Returns the count of the updated records """

    {"result": (query, update_data)}

    search(collection_name: str, user_search: str):
        """ Returns all records that match the user_search """
    {"result": API.db.search(collection_name, user_search)}


test_coverage(version, scan_collections, create, read, update, search)
