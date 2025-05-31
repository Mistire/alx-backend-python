#!/usr/bin/env python3

import unittest
from typing import Dict, List, Any
from parameterized import parameterized
from utils import access_nested_map

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

if '__main__' == __name__:
  unittest.main()