#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
  """A class to test access_nested_map function"""

  @parameterized.expand([
    ({"a": 1}, ["a"], 1),
    ({"a": {"b": 2}}, ["a"], {"b": 2}),
    ({"a": {"b": 2}}, ["a", "b"], 2),
  ])
  def test_access_nested_map(self, nested_map, path, expected):
    """A function to test access_nested_map function"""
    result = access_nested_map(nested_map, path)
    self.assertEqual(result, expected)

  @parameterized.expand([
    ({}, ["a"]),
    ({"a": 1}, ["a", "b"]),
  ])
  def test_access_nested_map_excpetion(self, nested_map, path):
    """A function to test access_nested_map function"""
    with self.assertRaises(KeyError):
      access_nested_map(nested_map, path)


if __name__ == '__main__':
  unittest.main()