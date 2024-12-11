from typing import Optional

class GitHubSettings:
    def __init__(self, username: str, token: str, repo_name: str, base_url: str, branch: str = "master"):
        """
        GitHub connection settings class.

        :param token: Personal access token for GitHub (recommended).
        :param username: GitHub username (if using basic authentication).
        :param password: GitHub password (if using basic authentication).
        """
        self.username = username
        self.token = token
        self.repo_name = repo_name
        self.base_url = base_url
        self.branch = branch
