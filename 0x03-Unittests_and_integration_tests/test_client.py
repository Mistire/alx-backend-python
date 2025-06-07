#!/usr/bin/env python3
import unittest
from unittest.mock import PropertyMock, patch
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

  def test_public_repos_url(self):
    """Test that _public_repos_url return correct URL from mocked org"""

    with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:

      mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
      client = GithubOrgClient('testorg')
      result = client._public_repos_url
      self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")


if '__main__' == __name__:
  unittest.main()