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

  @patch('client.get_json')
  @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
  def test_public_repos(self, mock_url, mock_get_json):
    """Test public_repos returns expected repo names"""
    mock_url.return_value = "http://mocked.url/repos"
    mock_get_json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"}
    ]

    client = GithubOrgClient("test")
    self.assertEqual(client.public_repos(), ["repo1", "repo2"])
    mock_get_json.assert_called_once_with("http://mocked.url/repos")

  

if '__main__' == __name__:
  unittest.main()