from abc import ABC, abstractmethod


class AbstractLogCacher(ABC):
    
    def __init__(self, prefix=None):
        pass
    
    @property
    @abstractmethod
    def display(self):
        pass
    
    @abstractmethod
    def cache_log(self, message):
        pass
    
    @abstractmethod
    def show_all_cached_logs(self):
        pass
    
    @abstractmethod
    def clear_cache(self):
        pass
