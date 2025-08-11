
import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.notify_dict.logger_setup import setup_logger


#REFACTOR: cache logs in NotifyDict and then use logger (less dependency and complexity)
#TODO: add how to use

class NotifyDict(dict):
    __slots__ = ["__cacheLogger",
                 "__enable_default_value",
                 "__default_value"]
    
    def __init__(self, logfile_name, logger_pid, enable_default_value=False, default_value=None, *args, **kwargs):
        cacheLogger = setup_logger(logfile_name=logfile_name, pid=logger_pid)
        self.__cacheLogger = cacheLogger
        self.__enable_default_value = enable_default_value
        self.__default_value = default_value
        
        dict.__init__(self, *args, **kwargs)
    
    def __getitem__(self, __key):
        return_default_value = self.__enable_default_value and (__key not in self.keys())
        if return_default_value:
            self.__cacheLogger.cache_log(f'__NO_SUCH_KEY__ (key:{__key}) | returning_default_value: {self.__default_value}')
            return self.__default_value
        return super().__getitem__(__key)
    
    def __setitem__(self, key, value):
        previous_value = self.get(key, '__NOT_EXISTS__')
        message = f'The key "{key}" setted to "{value}" from "{previous_value}"'
        self.__cacheLogger.cache_log(message)
        dict.__setitem__(self, key, value)
    
    def __delitem__(self, key):
        previous_value = self.get(key, '__NOT_EXISTS__')
        message = f'The key "{key}" deleted, previous_value: "{previous_value}"'
        self.__cacheLogger.cache_log(message)
        dict.__delitem__(self, key)
    
    def write_all_cached_logs(self):
        self.__cacheLogger.write_all_cached_logs()
    
    def clear_all_cached_logs(self):
        self.__cacheLogger.clear_cache()
    
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
