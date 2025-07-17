#!/usr/bin/env python3
import unittest

from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
"""Unit tests for utils.py functions."""
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

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, expected, mock_get):
        """A function to test get_json function"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        result = get_json(url)
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """A class to test memoize function"""

    def test_memoize(self):
        """A function to test memoize function"""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock:
            test_instance = TestClass()
            test_instance.a_property
            test_instance.a_property
            mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
