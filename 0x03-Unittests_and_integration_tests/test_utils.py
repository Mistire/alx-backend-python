#!/usr/bin/env python3
import unittest

from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json

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
  def test_access_nested_map_exception(self, nested_map, path):
    """A function to test access_nested_map function"""
    with self.assertRaises(KeyError):
      access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
  """A class to test get_json function"""

  @patch('utils.requests.get')
  def test_get_json(self, mock_get):
    """A function to test get_json function"""
    def mock_get_side_effect(url):
      mock_response = Mock()
      if url == "http://example.com":
        mock_response.json.return_value = {"payload": "True"}
      elif url == "http://holberton.io":
        mock_response.json.return_value = {"payload": "False"}
      else:
        mock_response.json.return_value = {"error": "not found"}
      return mock_response
    
    mock_get.side_effect = mock_get_side_effect

    result1 = get_json("http://example.com")
    self.assertEqual(result1, {"payload": "True"})
    result2 = get_json("http://holberton.io")
    self.assertEqual(result2, {"payload": "False"})

    self.assertEqual(mock_get.call_count, 2)
    mock_get.assert_any_call("http://example.com")
    mock_get.assert_any_call("http://holberton.io")



if __name__ == '__main__':
  unittest.main()