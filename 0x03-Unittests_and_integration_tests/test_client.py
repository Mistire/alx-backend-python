#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
  """Test different GithubOrg functionality"""
  @parameterized.expand([
    ('google',),
    ('abc',)
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
    """Test GithubOrgClient.org returns expected returns"""
    expected = {"login": org_name}
    mock_get_json.return_value = expected

    client = GithubOrgClient(org_name)
    self.assertEqual(client.org, expected)
    mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

if '__main__' == __name__:
  unittest.main()