



def test_coverage():

    '''
    >>> from app.api import version, scan_collections, create, read, update, search
    >>> from app.api import API
    >>> import requests
    >>> version_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/version'
    >>> scan_collections_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/scan_collections'
    >>> create_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/create'
    
    >>> read_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/read'
    >>> update_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/update'
    >>> search_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/search'
    >>> requests.get(version_link)
    
    <Response [200]>
    
    >>> requests.get(version_link).json()==version()
    True

    >>> requests.get(scan_collections_link)
    <Response [200]>
    >>> requests.get(scan_collections_link).json()==scan_collections()
    True
    '''
test_coverage()

if __name__ == "__main__":

    import doctest
    doctest.testmod()


    # create({"result": API.db.create(collection_name, data)})
    # """ Creates a new record
    #     (collection_name: str, data: Dict)"""

    # read({"result": API.db.read(collection_name, data)})
    # """ Returns records based on query
    #     (collection_name: str, data: Dict)"""

    # update(collection_name: str, query: Dict, update_data: Dict):
    # """ Returns the count of the updated records """

    # {"result": (query, update_data)}


    # search(collection_name: str, user_search: str):
    #     """ Returns all records that match the user_search """
    # {"result": API.db.search(collection_name, user_search)}
    # test_coverage(version, scan_collections, create, read, update, search)
