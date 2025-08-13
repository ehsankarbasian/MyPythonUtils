from abc import ABC, abstractmethod
import copy


class AbstractLogCacher(ABC):
    
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def display_function(cls, text):
        pass
    
    @property
    @abstractmethod
    def iterable_cached_logs(self):
        pass
    
    @iterable_cached_logs.setter
    def iterable_cached_logs(self, value):
        self.__iterable_cached_logs = copy.copy(value)
    
    @iterable_cached_logs.getter
    def iterable_cached_logs(self):
        return self.__iterable_cached_logs
    
    @abstractmethod
    def cache_log(self, message):
        pass
    
    @abstractmethod
    def clear_cache(self):
        pass
    
    def show_all_cached_logs(self):
        for line in self.iterable_cached_logs:
            self.display_function(line)
