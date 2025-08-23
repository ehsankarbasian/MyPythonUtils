from unittest import TestCase
import unittest
import glob

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.test_tools.fixture_loaders.mongo_loader import mongoLoader


# TODO: Read and Debug
# TODO: Complete README

class FixtureSupporterTestCase(TestCase):
    
    # Only change this attribute to install fixture_type to be load for tests. No need to change other codes in this class.
    # Call the loader in generalLoader too.
    __INSTALLED_FIXTURES = {
        'mongo': mongoLoader,
    }
    
    
    def __init__(self, methodName):
        self.general_fixtures = dict()
        for fixture_name in list(self.__INSTALLED_FIXTURES.keys()):
            self.general_fixtures[fixture_name] = self.__get_fixtures(fixture_name)
        
        super().__init__(methodName)
    
    
    def __get_fixtures(self, fixture_name):
        fixtures_string = f'{fixture_name}_fixtures'
        fixtures_path_string = f'{fixture_name}_fixtures_path'
        result_fixtures = list()
        if hasattr(self, fixtures_string) and hasattr(self, fixtures_path_string):
            fixtures = getattr(self, fixtures_string)
            fixtures_path = getattr(self, fixtures_path_string)
            all_fixtures = self.__get_fixture_file_names(fixtures_path=fixtures_path)
            if fixtures == '__all__':
                return all_fixtures
            else:
                fixture_filenames = [name.split('/')[-1] for name in all_fixtures]
                for name in fixture_filenames:
                    if name in fixtures:
                        result_fixtures.append(f'{fixtures_path}/{name}')
                        
        return result_fixtures
    
    
    def __get_fixture_file_names(self, fixtures_path):
        fixture_filenames = glob.glob(f'{fixtures_path}/*.json')
        return fixture_filenames
    
    
    def load_fixtures(self):
        for fixture_type, fixture_files in self.general_fixtures.items():
            loaderClass = self.__INSTALLED_FIXTURES[fixture_type]
            loaderClass.load_fixtures(fixture_files)
    
    
    def clear_fixtures(self):
        for fixture_type, fixture_files in self.general_fixtures.items():
            loaderClass = self.__INSTALLED_FIXTURES[fixture_type]
            loaderClass.clear_fixtures(fixture_files)
    
    
    @staticmethod
    def get_file_directory_adderss(file_address):
        # file_address must be __file__ in any file uses this function
        directory_address = '/'.join(file_address.split('/')[:-1])
        return directory_address


# TODO: Complete the how_to_use section

def _add(a, b):
    return a + b


class AddTestCase(FixtureSupporterTestCase):
    
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_add_1(self):
        self.assertEqual(_add(3, 7), 10)
    
    def test_add_2(self):
        self.assertEqual(_add(3, -7), -4)
    
    # Use fixtures
    def test_add_read_from_mongo(self):
        pass


if __name__=='__main__':
    unittest.main()
