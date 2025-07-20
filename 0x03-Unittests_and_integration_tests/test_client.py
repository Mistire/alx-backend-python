#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import PropertyMock, patch, Mock
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

  def test_public_repos_url(self):
    """Test that _public_repos_url returns correct URL"""
    expected = "https://api.github.com/orgs/testorg/repos"

    with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
      mock_org.return_value = {"repos_url": expected}
      client = GithubOrgClient("testorg")
      self.assertEqual(client._public_repos_url, expected)

  

if '__main__' == __name__:
  unittest.main()