#!/usr/bin/env python3
"""
This module contains unit tests for the utility functions:
- access_nested_map
- get_json
- memoize
"""

import unittest
from typing import Dict, List, Any
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit test for the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: List[str], expected
    ):
        """
        Test that `access_nested_map` returns the correct value when
        given valid nested maps and path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"])
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: List[str]
    ) -> None:
        """
        Test that `access_nested_map` raises a KeyError when the path
        doesn't exist in the nested map.
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
        """Test that get_json fetches correct value"""
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('requests.get', **config)
        mock = patcher.start()
        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patcher.stop()


class TestMemoize(unittest.TestCase):
    """Unit tests for the `memoization` function from the `utils` module."""

    def test_memoize(self):
        """Test that memoize caches the result of a method call."""
        class TestClass:
            """A Test Class for handling methods that memonize"""

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


if __name__ == '__main__':
    unittest.main()
