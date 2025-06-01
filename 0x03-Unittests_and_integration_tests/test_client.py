#!/usr/bin/env python3
"""Unit tests and integration tests for GithubOrgClient"""

import unittest
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


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
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock)
    def test_public_repos_url(self, mock_public_repos_url):
        """Test _public_repos_url property"""
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )
        client = GithubOrgClient("google")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/google/repos"
        )


class TestGithubOrgClientPublicRepos(unittest.TestCase):
    """Unit test for public_repos method"""

    @patch("client.get_json", return_value=[
        {"name": "repo1", "license": {"key": "MIT"}},
        {"name": "repo2", "license": {"key": "Apache-2.0"}},
        {"name": "repo3", "license": None}
    ])
    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos method"""
        mock_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )
        client = GithubOrgClient("google")

        self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
        self.assertEqual(client.public_repos(license="MIT"), ["repo1"])
        self.assertEqual(
            client.public_repos(license="Apache-2.0"),
            ["repo2"]
        )
        self.assertEqual(client.public_repos(license="GPL"), [])

        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once()


class TestGithubOrgClientHasLicense(unittest.TestCase):
    """Unit test for has_license"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
        ({"other_key": "value"}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license logic"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([{
    "org_payload": {
        "repos_url": "https://api.github.com/orgs/google/repos"
    },
    "repos_payload": [
        {"name": "repo1", "license": {"key": "MIT"}},
        {"name": "repo2", "license": {"key": "Apache-2.0"}}
    ],
    "expected_repos": ["repo1", "repo2"],
    "apache2_repos": ["repo2"]
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test using parameterized_class"""

    @classmethod
    def setUpClass(cls):
        """Patch get_json for integration test"""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                return cls.repos_payload
            return {}

        cls.mock_get_json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="Apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
