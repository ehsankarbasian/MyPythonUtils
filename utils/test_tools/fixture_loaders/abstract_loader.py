from abc import ABC, abstractmethod


class AbstractLoader(ABC):
    
    def load_fixtures(self, fixture_files):
        for file_address in fixture_files:
            self._load_fixture(file_address)
    
    def clear_fixtures(self, fixture_files):
        for file_address in fixture_files:
            self._clear_fixture(file_address)
    
    @abstractmethod
    def _load_fixture(self, file_address):
        pass
    
    @abstractmethod
    def _clear_fixture(self, file_address):
        pass
