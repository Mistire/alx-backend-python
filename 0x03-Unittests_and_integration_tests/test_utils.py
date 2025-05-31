#!/usr/bin/env python3

import unittest
from typing import Dict, List, Any
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
  """Unit tests for the `access_nested_map` function from the `utils` module."""
  
  @parameterized.expand([
    ({"a": 1}, ["a"], 1),
    ({"a": {"b": 2}}, ["a"], {"b": 2}),
    ({"a": {"b": 2}}, ["a", "b"], 2),
  ])
  def test_access_nested_map(self, nested_map: Dict[str, Any], path: List[str], expected):
    """
    Test that `access_nested_map` returns the correct value when given valid nested maps and path. 
    """
    self.assertEqual(access_nested_map(nested_map, path), expected) 


  @parameterized.expand([
    ({}, ["a"]),
    ({"a": 1}, ["a", "b"])
  ])
  def test_access_nested_map_exception(self, nested_map: Dict[str, Any], path: List[str]) -> None:
    """
    Test that `access_nested_map` raises a KeyError when the path doesn't exist in the nested map.
    """
    with self.assertRaises(KeyError):
      access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
  """Unit test for the `get_json` function in `utils`"""

  @parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False}),
  ])
  def test_get_json(self, test_url, test_payload):
    """Test get_json"""
    config = {'return_value.json.return_value': test_payload}
    patcher = patch('requests.get', **config)
    mock = patcher.start()
    self.assertEqual(get_json(test_url), test_payload)
    mock.assert_called_once()
    patcher.stop()

class TestMemoize(unittest.TestCase):

  def test_memoize(self):
    class TestClass:

      def a_method(self):
        return 42
      
      @memoize
      def a_property(self):
        return self.a_method()
      
    with patch.object(TestClass, "a_method") as mock:
      test_class = TestClass()
      test_class.a_property()
      test_class.a_property()
      mock.assert_called_once()
      
  




if '__main__' == __name__:
  unittest.main()