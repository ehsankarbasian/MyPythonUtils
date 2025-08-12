from abc import ABC, abstractmethod
import copy


class AbstractLogCacher(ABC):
    
    def __init__(self, prefix=None):
        pass
    
    @property
    @abstractmethod
    def display_function(self):
        pass
    
    # TODO: Make it private
    @property
    @abstractmethod
    def iterable_cached_logs(self):
        pass
    
    @iterable_cached_logs.setter
    def iterable_cached_logs(self, value):
        self.iterable_cached_logs = copy.copy(value)
    
    @abstractmethod
    def cache_log(self, message):
        pass
    
    @abstractmethod
    def clear_cache(self):
        pass
    
    def show_all_cached_logs(self):
        for line in self.iterable_cached_logs:
            self.display_function(line)
