from utils.log_cacher.abstract_cacher import AbstractLogCacher


class RedisLogCacher(AbstractLogCacher):
    
    def __init__(self, redis_client, cache_list_name, prefix=None):
        self.__redis_client = redis_client
        self.__cache_list_name = cache_list_name
        self._prefix = prefix
    
    def cache_log(self, message):
        if self._prefix:
            message = f'{self._prefix} | {message}'
        self.__redis_client.lpush(self.__cache_list_name, message)
    
    @classmethod
    def display_function(cls, text):
        print(text.decode('utf-8'))
    
    @property
    def iterable_cached_logs(self):
        return self.__redis_client.lrange(self.__cache_list_name, 0, -1)[::-1]
    
    def clear_cache(self):
        self.__redis_client.delete(self.__cache_list_name)
