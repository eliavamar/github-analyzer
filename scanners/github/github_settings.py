from typing import Optional

class GitHubSettings:
    def __init__(self, token: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        """
        GitHub connection settings class.

        :param token: Personal access token for GitHub (recommended).
        :param username: GitHub username (if using basic authentication).
        :param password: GitHub password (if using basic authentication).
        """
        self.token = token
        self.username = username
        self.password = password
