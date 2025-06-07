#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

  @parameterized.expand([
    ("google",),
    ("abc",)
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
    """Test GIthubOrgClient.org return expected result"""
    expected = {"login": org_name}
    mock_get_json.return_value = expected

    client = GithubOrgClient(org_name)
    self.assertEqual(client.org, expected)
    mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")



if '__main__' == __name__:
  unittest.main()