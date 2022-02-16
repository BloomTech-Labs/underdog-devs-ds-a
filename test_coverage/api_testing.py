def test():
    '''
        >>> requests.get(version_link)
        <Response [200]>
        >>> requests.get(version_link).json()
        {'result': '0.0.2'}
    '''

if __name__ == "__main__":
    import doctest
    import requests
    from app import api

    version_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/version'
    scan_collections_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/scan_collections'
    create_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/create'
    read_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/read'
    update_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/update'
    search_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/search'
    doctest.testmod(name='test', verbose=True)
