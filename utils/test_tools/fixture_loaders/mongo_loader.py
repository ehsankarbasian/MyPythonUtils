import json

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute())
sys.path.append(path)

from utils.test_tools.fixture_loaders.abstract_loader import AbstractLoader
from utils.test_tools.mocked_mongo.mocked_mongo import get_mongo_mocked_colletion


class __MongoLoader(AbstractLoader):
    
    def __get_mongo_collection_name(self, file_address):
        file_name = file_address.split('/')[-1]
        collection_name = file_name.replace('.json', '')
        return collection_name

    def _load_fixture(self, file_address):
        with open(file_address, "r", encoding="utf8") as file:
            data = json.load(file)
            collection_name = self.__get_mongo_collection_name(file_address)
            collection = get_mongo_mocked_colletion(collection_name)
            collection.insert_many(data)
    
    def _clear_fixture(self, file_address):
        collection_name = self.__get_mongo_collection_name(file_address)
        collection = get_mongo_mocked_colletion(collection_name)
        collection.delete_many({})


mongoLoader = __MongoLoader()
