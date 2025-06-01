#!/usr/bin/env python3
"""Unit tests and integration tests for GithubOrgClient"""

import unittest
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict


# Unit test for GithubOrgClient.org
class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_output, mock_get_json):
        """Test GithubOrgClient.org method"""
        mock_get_json.return_value = expected_output
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_output)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_public_repos_url):
        """Test _public_repos_url property"""
        mock_public_repos_url.return_value = f"https://api.github.com/orgs/google/repos"
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, f"https://api.github.com/orgs/google/repos")


# More patching
class TestGithubOrgClientPublicRepos(unittest.TestCase):
    """Unit-test GithubOrgClient.public_repos"""

    @patch("client.get_json", return_value=[
        {"name": "repo1", "license": {"key": "MIT"}},
        {"name": "repo2", "license": {"key": "Apache-2.0"}},
        {"name": "repo3", "license": None}
    ])
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos method"""
        mock_repos_url.return_value = f"https://api.github.com/orgs/google/repos"
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
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
        ({"other_key": "value"}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license behavior, ensuring proper edge case handling."""
        self.assertEqual(GithubOrgClient.has_license.__func__(repo, license_key), expected)




@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0][0],  # Organization data
     "repos_payload": TEST_PAYLOAD[0][1],  # List of repos
     "expected_repos": [repo["name"] for repo in TEST_PAYLOAD[0][1]],
     "apache2_repos": [
         repo["name"] for repo in TEST_PAYLOAD[0][1]
         if repo.get("license", {}).get("key") == "Apache-2.0"
     ]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Mock external requests before tests"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Ensure class attributes exist
        cls.org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        cls.repos_payload = [{"name": "repo1"}, {"name": "repo2"}]
        cls.expected_repos = ["repo1", "repo2"]
        cls.apache2_repos = []

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
        """
        Initialize MockResponse with a JSON payload.

        Args:
            json_data (dict, optional): The mock JSON response data.
        """
        self.json_data = json_data if json_data is not None else {}

    def json(self):
        """Return the mock JSON response."""
        return self.json_data


# Run all tests
if __name__ == "__main__":
    unittest.main()
