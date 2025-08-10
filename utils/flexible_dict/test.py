from unittest import TestCase
import unittest

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.flexible_dict.flexible_dict import FlexibleDict, _SubscriptableDefault


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
    
    def test_interable_access_level_1(self):
        pass
    
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


class FlexibleDictStructureTestCase(TestCase):
    
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
    
    def test_final_value_type(self):
        self.assertIsInstance(self.flexible_dict['a'].value, str)
        self.assertIsInstance(self.flexible_dict['a'].flexible_value.value, str)
        self.assertIsInstance(self.flexible_dict['cdefg'].value, dict)
        self.assertIsInstance(self.flexible_dict['cdefg'].flexible_value.value, dict)
    
    def test_inner_value_is_flexible(self):
        self.assertIsInstance(self.flexible_dict['cdefg']['defg'], FlexibleDict)
        self.assertIsInstance(self.flexible_dict['cdefg']['c'], _SubscriptableDefault)
    
    def test_inner_value_is_not_flexible_after_dotvalue(self):
        self.assertNotIsInstance(self.flexible_dict['cdefg'].value['defg'], FlexibleDict)
        self.assertNotIsInstance(self.flexible_dict['cdefg'].value['c'], _SubscriptableDefault)
    
    def test_flexible_value_type(self):
        self.assertIsInstance(self.flexible_dict['a'].flexible_value, _SubscriptableDefault)
        self.assertIsInstance(self.flexible_dict['cdefg'].flexible_value, FlexibleDict)
    
    def test_chained_flexible_value_type(self):
        self.assertIsInstance(self.flexible_dict['a'].flexible_value.flexible_value, _SubscriptableDefault)
        self.assertIsInstance(self.flexible_dict['cdefg'].flexible_value.flexible_value, FlexibleDict)
    
    def test_flexible_value_chain(self):
        level_1 = self.flexible_dict['a'].flexible_value
        level_2 = level_1.flexible_value
        level_3 = level_2.flexible_value
        self.assertEqual(level_1.__dict__, level_2.__dict__)
        self.assertEqual(level_2.__dict__, level_3.__dict__)
        self.assertNotEqual(level_1, level_2)
        self.assertNotEqual(level_2, level_3)
        self.assertEqual(level_1.value, 'a')
        self.assertEqual(level_2.value, 'a')
        self.assertEqual(level_3.value, 'a')
    
    def test_flexible_value_not_changes_the_final_value(self):
        final_value = self.flexible_dict['a'].value
        final_value_with_flexible_in_middle = self.flexible_dict['a'].flexible_value.value
        self.assertEqual(final_value, final_value_with_flexible_in_middle)
    
    def test_final_value_type_after_setitem(self):
        self.flexible_dict['cdefg'] = {'f': 'f', 'g': 'g'}
        self.assertIsInstance(self.flexible_dict['cdefg'], dict)
        self.assertIsInstance(self.flexible_dict['cdefg'], FlexibleDict)
        
        self.assertIsInstance(self.flexible_dict['cdefg'].value, dict)
        self.assertNotIsInstance(self.flexible_dict['cdefg'].value, FlexibleDict)
        self.assertNotIsInstance(self.flexible_dict['cdefg'].value, _SubscriptableDefault)
        
        self.assertIsInstance(self.flexible_dict['cdefg'].flexible_value.value, dict)
        self.assertNotIsInstance(self.flexible_dict['cdefg'].flexible_value.value, FlexibleDict)
        self.assertNotIsInstance(self.flexible_dict['cdefg'].flexible_value.value, _SubscriptableDefault)
        
        self.assertIsInstance(self.flexible_dict['cdefg']['f'], _SubscriptableDefault)
        self.assertIsInstance(self.flexible_dict['cdefg']['f'].value, str)
        self.assertNotIsInstance(self.flexible_dict['cdefg']['f'].value, _SubscriptableDefault)
        self.assertIsInstance(self.flexible_dict['cdefg']['f'].flexible_value.value, str)
    
    def test_flexible_value_type_after_setitem(self):
        self.flexible_dict['cdefg'] = {'f': 'f', 'g': 'g'}
        self.assertIsInstance(self.flexible_dict['cdefg'].flexible_value, FlexibleDict)
        self.assertIsInstance(self.flexible_dict['cdefg']['f'].flexible_value, _SubscriptableDefault)
        self.assertIsInstance(self.flexible_dict['cdefg']['f']['n'].flexible_value, _SubscriptableDefault)
    
    def test_item_setted_after_setitem_level_1(self):
        item = {'f': 'f', 'g': 'g'}
        self.flexible_dict['cdefg'] = item
        self.assertEqual(self.flexible_dict['cdefg'].value, item)
        self.assertEqual(self.flexible_dict['cdefg'].flexible_value.value, item)
    
    def test_item_setted_after_setitem_level_2(self):
        item = {'f': 'f', 'g': 'g'}
        self.flexible_dict['cdefg'] = item
        self.flexible_dict['cdefg']['f'] = 'new'
        self.assertIsInstance(self.flexible_dict['cdefg']['f'], _SubscriptableDefault)
        self.assertEqual(self.flexible_dict['cdefg']['f'].value, 'new')
        self.assertEqual(self.flexible_dict['cdefg']['f'].flexible_value.value, 'new')
    
    def test_flexible_relation_disconnection_after_call_dotvalue(self):
        self.flexible_dict['cdefg'] = {'f': 'f', 'g': 'g'}
        self.flexible_dict['cdefg'].value['f'] = 'new'
        self.assertNotEqual(self.flexible_dict['cdefg']['f'].value, 'new')
        self.assertEqual(self.flexible_dict['cdefg']['f'].value, 'f')


if __name__=='__main__':
    unittest.main()
