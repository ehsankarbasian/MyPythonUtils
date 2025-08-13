# pip install mongomock

import mongomock
client = mongomock.MongoClient()


def get_mongo_mocked_colletion(collection_name, database_name='my_database'):
    database = client.__getattr__(database_name)
    collection = database.__getattr__(collection_name)
    return collection


class __MockedTunnel:
    def close(self):
        pass

mocked_tunnel = __MockedTunnel()


def close_mongo_mocked(tunnel=None, collection=None):
    tunnel.close()
    collection.drop()
