from utils.log_cacher.abstract_cacher import AbstractLogCacher


class SimpleLogCacher(AbstractLogCacher):
    
    def __init__(self, prefix=None):
        self._cache = []
        self._prefix = prefix
    
    def cache_log(self, message):
        if self._prefix:
            message = f'{self._prefix} | {message}'
        self._cache.append(message)
    
    def show_all_cached_logs(self):
        for line in self._cache:
            print(line)
    
    def clear_cache(self):
        self._cache = list()
