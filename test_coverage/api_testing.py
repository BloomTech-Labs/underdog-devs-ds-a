
'''
>>> str(requests.get(version_link))=='<Response [200]>'
True
>>> requests.get(version_link).json()=={'result': '0.0.2'}
True

'''

if __name__ == "__main__":
    version_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/version'
    scan_collections_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/scan_collections'
    create_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/create'
    read_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/read'
    update_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/update'
    search_link = 'http://underdog-devs-ds-a-dev.us-east-1.elasticbeanstalk.com/search'
    import requests
    from app.api import API
    from app.api import version, collections

    import doctest
    doctest.testmod()
