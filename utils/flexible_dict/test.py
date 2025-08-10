from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.flexible_dict.flexible_dict import FlexibleDict


class FlexibleDictBehaviourTestCase(TestCase):
    
    def setUp(self):
        default_dict = {'a': 'a',
                        'c': 30,
                        'b': 'b',
                        'cdefg': {
                            'c': 'c',
                            'defg': {
                                'd': 'd',
                                'efg':{
                                    'e': 'e',
                                    'fg': {'f': 'f', 'g': 'g'}
                                    }
                                }
                            },
                        }
        self.flexible_dict = FlexibleDict(input_dict=default_dict,
                                          default='__MY_NONE__',
                                          iterable_default='__MY_ITERABLE_DEFAULT__')
    
    
    def tearDown(self):
        return super().tearDown()
    
    def test_simple_access_level_1(self):
        self.assertEqual(self.flexible_dict['a'].value, 'a')
        self.assertEqual(self.flexible_dict['b'].value, 'b')
        self.assertEqual(self.flexible_dict['c'].value, 30)
    
    def test_simple_access_level_2(self):
        self.assertEqual(self.flexible_dict['cdefg']['c'].value, 'c')
    
    def test_simple_access_level_3(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['d'].value, 'd')
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg'].value, {'e': 'e', 'fg': {'f': 'f', 'g': 'g'}})
    
    def test_simple_access_level_4(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg']['e'].value, 'e')
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg']['fg'].value, {'f': 'f', 'g': 'g'})
    
    def test_simple_access_level_5(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg']['fg']['f'].value, 'f')
    
    def test_not_exists_access_level_1(self):
        self.assertEqual(self.flexible_dict['d'].value, '__MY_NONE__')
    
    def test_not_exists_access_level_2(self):
        self.assertEqual(self.flexible_dict['b']['c'].value, '__MY_NONE__')
    
    def test_not_exists_access_level_3(self):
        self.assertEqual(self.flexible_dict['b']['c']['k'].value, '__MY_NONE__')
        self.assertEqual(self.flexible_dict['cdefg']['defg']['kk'].value, '__MY_NONE__')
    
    def test_not_exists_access_level_4(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['kk']['hh'].value, '__MY_NONE__')
        
    def test_not_exists_access_level_5(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg']['fg']['k'].value, '__MY_NONE__')
        
    def test_not_exists_access_level_6(self):
        self.assertEqual(self.flexible_dict['cdefg']['defg']['efg']['fg']['g']['k'].value, '__MY_NONE__')


if __name__=='__main__':
    unittest.main()
