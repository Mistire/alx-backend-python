#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""
import unittest
from unittest.mock import PropertyMock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test different GithubOrg functionality"""
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected result"""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL"""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient('testorg')
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/testorg/repos"
            self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        client_github = 'client.GithubOrgClient._public_repos_url'

        with patch(client_github, new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://mocked.url/repos"
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])

            mock_get_json.assert_called_once_with("http://mocked.url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test if GithubOrgClient returns the right output for has_license"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)

if __name__ == '__main__':
    unittest.main()
