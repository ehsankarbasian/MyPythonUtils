
#REFACTOR: Use as separate module
class LogCacher:
    
    def __init__(self, prefix=None):
        self._cache = []
        self._prefix = prefix
    
    def cache_log(self, message):
        if self._prefix:
            message = f'{self._prefix} | {message}'
        self._cache.append(message)
    
    # TODO: Strategy pattern
    def print_all_cached_logs(self):
        for line in self._cache:
            print(line)
    
    def clear_cache(self):
        self._cache = list()


class NotifyDict(dict):
    __slots__ = ["__logCacher",
                 "__enable_default_value",
                 "__default_value"]
    
    def __init__(self, logfile_name, logger_pid, enable_default_value=False, default_value=None, *args, **kwargs):
        prefix = f'{logger_pid} | {logfile_name}'
        self.__logCacher = LogCacher(prefix=prefix)
        self.__enable_default_value = enable_default_value
        self.__default_value = default_value
        
        dict.__init__(self, *args, **kwargs)
    
    def __getitem__(self, __key):
        return_default_value = self.__enable_default_value and (__key not in self.keys())
        if return_default_value:
            self.__logCacher.cache_log(f'__NO_SUCH_KEY__ (key:{__key}) | returning_default_value: {self.__default_value}')
            return self.__default_value
        return super().__getitem__(__key)
    
    def __setitem__(self, key, value):
        previous_value = self.get(key, '__NOT_EXISTS__')
        message = f'The key "{key}" setted to "{value}" from "{previous_value}"'
        self.__logCacher.cache_log(message)
        dict.__setitem__(self, key, value)
    
    def __delitem__(self, key):
        previous_value = self.get(key, '__NOT_EXISTS__')
        message = f'The key "{key}" deleted, previous_value: "{previous_value}"'
        self.__logCacher.cache_log(message)
        dict.__delitem__(self, key)
    
    def write_all_cached_logs(self):
        self.__logCacher.print_all_cached_logs()
    
    def clear_all_cached_logs(self):
        self.__logCacher.clear_cache()
    
    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self.log_callback('a change !')
            return result
        return wrapper
    
    clear = _wrap(dict.clear)
    pop = _wrap(dict.pop)
    popitem = _wrap(dict.popitem)
    setdefault = _wrap(dict.setdefault)
    update =  _wrap(dict.update)
