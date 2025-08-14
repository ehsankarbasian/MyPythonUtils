from utils.test_tools.mocked_mongo.mocked_mongo import get_mongo_mocked_colletion, close_mongo_mocked
from utils.log_cacher.abstract_cacher import AbstractLogCacher


class MongoLogCacher(AbstractLogCacher):
    _MESSAGE_KEY = 'message'
    
    def __init__(self, mongo_collection_name, prefix=None):
        collection = get_mongo_mocked_colletion(mongo_collection_name)
        
        self._cache = collection
        self._prefix = prefix
    
    def cache_log(self, message):
        if self._prefix:
            message = f'{self._prefix} | {message}'
        self._cache.insert_one({self._MESSAGE_KEY: message})
    
    def display_function(self, text):
        print(text[self._MESSAGE_KEY])
    
    @property
    def iterable_cached_logs(self):
        return self._cache.find()
    
    def clear_cache(self):
        self._cache.drop()
