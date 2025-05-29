#!/usr/bin/env python3
"""Unit tests and integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


# More patching
class TestGithubOrgClientPublicRepos(unittest.TestCase):
    """Unit-test GithubOrgClient.public_repos"""

    @patch("client.get_json", return_value=[
        {"name": "repo1", "license": {"key": "MIT"}},
        {"name": "repo2", "license": {"key": "Apache-2.0"}},
        {"name": "repo3", "license": None},
    ])
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock, return_value="https://api.github.com/orgs/google/repos")
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos method"""
        client = GithubOrgClient("google")

        # Test all public repos
        self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])

        # Test license filtering
        self.assertEqual(client.public_repos(license="MIT"), ["repo1"])
        self.assertEqual(client.public_repos(license="Apache-2.0"), ["repo2"])
        self.assertEqual(client.public_repos(license="GPL"), [])  # No match

        # Ensure mocks were called once
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once()


# Parameterized test for has_license
class TestGithubOrgClientHasLicense(unittest.TestCase):
    """Unit-test GithubOrgClient.has_license"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license behavior"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": {"repos_url": "https://api.github.com/orgs/google/repos"},
     "repos_payload": [{"name": "repo1"}, {"name": "repo2"}],
     "expected_repos": ["repo1", "repo2"],
     "apache2_repos": []}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Mock external requests before tests"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)


class MockResponse:
    """Mock requests.get response"""

    def __init__(self, json_data=None):
        self.json_data = json_data if json_data is not None else {}

    def json(self):
        return self.json_data


# Run all tests
if __name__ == "__main__":
    unittest.main()