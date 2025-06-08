#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""
import unittest
from unittest.mock import PropertyMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

class MockResponse:
    """A Class for making mock response"""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


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




@parameterized_class(

        ("org_payload",
        "repos_payload",
        "expected_repos",
        "apache2_repos"), TEST_PAYLOAD
    
)
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        # def my_side_effect(url):
        #     """ Side Effect function for test """
        #     test_url = "https://api.github.com/orgs/google"
        #     if url == test_url:
        #         return cls.org_payload
        #     return cls.repos_payload

        config = {'return_value.json.side_effect':
                [
                    cls.org_payload, cls.repos_payload,
                    cls.org_payload, cls.repos_payload
                ]
        }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()

if "__main__" == __name__:
    unittest.main()