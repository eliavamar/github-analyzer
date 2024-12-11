import os

from git import Tag
from github import Github, Auth, PaginatedList
import git
import re

from scanners.github.FileChangeInfo import FileChangeInfo
from scanners.github.github_settings import GitHubSettings


##TODO: check close the git client


class GitHubScanner:
    ##TODO: The __init__ need to get the settings.py
    def __init__(self, github_settings: GitHubSettings):
        self.auth = Auth.Token(github_settings.token)
        self.github_settings = github_settings
        if github_settings.base_url:
            ##TODO: why its not work without the verify=False
            self.github = Github(auth=self.auth, base_url=github_settings.base_url, verify=False)
        else:
            self.github = Github(auth=self.auth)

        self.repo_metadata = self.get_repo_metadata()

    def get_repo_metadata(self):
        ##TODO: get_repo(name) not work checkout why
        for optional_rep in self.github.get_user().get_repos():
            if self.github_settings.repo_name == optional_rep.full_name:
                return optional_rep
        raise Exception("The repo not exist")

    def get_repo_auth_url(self):
        auth_url = self.repo_metadata.clone_url.replace("https://", f"https://{self.github_settings.username}:{self.auth.token}@")
        return auth_url

    def clone_repo(self, branch="main", clone_path=None):
        """Clones the repository at a specific branch to repo_dir path."""
        repo_dir = f"/tmp/{self.github_settings.repo_name}"
        auth_url = self.get_repo_auth_url()
        if clone_path is not None:
            repo_dir = clone_path
        if os.path.exists(repo_dir):
            print("Repository already cloned, pulling latest changes.")
            repo = git.Repo(repo_dir)
            repo.git.checkout(branch)  # Checkout the specified version
            repo.remotes.origin.set_url(auth_url).pull()  # Ensure it's up to date
        else:
            print("Cloning repository.")
            repo = git.Repo.clone_from(auth_url, repo_dir, branch=branch)
        return repo

    def get_releases(self):
        """Returns the list of releases in descending order."""
        releases = self.repo_metadata.get_releases()
        return sorted(releases, key=lambda release: release.published_at, reverse=True)

    def get_tags(self):
        """Returns  tags in descending order based on creation date."""
        tags: PaginatedList[Tag] = self.repo_metadata.get_tags()  # Get all tags
        return tags

    def get_recent_two_tags(self):
        """
        Returns the two most recent tags based on their commit date.
        """
        tags = self.get_tags()
        # Sort the tags by commit date (most recent first)
        sorted_tags = sorted(tags, key=lambda tag: tag.commit.committer.last_modified_datetime, reverse=True)

        # Get the most recent two tags
        most_recent_two_tags = sorted_tags[:2]

        return most_recent_two_tags

    def get_diff_between_tags(self, tag1: Tag, tag2: Tag, main_repo_branch: str):
        """
        Gets the diff between two tags in the repository using their commit SHAs.
        """
        if not self.repo_metadata:
            raise ValueError("Repository is not defined.")

        try:
            # Get the commit SHAs for both tags
            sha1 = tag1.commit.sha
            sha2 = tag2.commit.sha

            # Clone the repo to a temporary location (assuming `clone_repo` returns a Repo object)
            temp_repo = self.clone_repo(main_repo_branch)

            # Get the actual diff as text
            diff_text = temp_repo.git.diff(sha1, sha2)

            # Split the diff text by file changes using the pattern for "diff --git" lines
            file_diffs = re.split(r'(^diff --git a/.*? b/.*?$)', diff_text, flags=re.MULTILINE)

            # Pair the diff headers and content using a dictionary for efficient lookup
            diffs = {}
            for i in range(1, len(file_diffs), 2):
                header = file_diffs[i]
                content = file_diffs[i + 1]
                match = re.search(r'diff --git a/(.*?) b/', header)
                if match:
                    file_path = match.group(1)
                    diffs[file_path] = header + content

            # Get the diff info (metadata) between the two commits
            diff_info = temp_repo.commit(sha1).diff(temp_repo.commit(sha2))

            # List to store the final result
            result: list[FileChangeInfo] = []

            for diff_item in diff_info:
                file_path = diff_item.a_path or diff_item.b_path
                change_type = diff_item.change_type

                # Find the corresponding diff content based on the file path
                if file_path in diffs:
                    file_change = FileChangeInfo(file_path=file_path,
                                                     change_type=change_type,
                                                     change_content=diffs[file_path])
                    result.append(file_change)

            return result

        except git.GitCommandError as e:
            raise RuntimeError(f"Git command error while comparing tags {tag1.name} and {tag2.name}: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error comparing tags {tag1.name} and {tag2.name}: {str(e)}")

    def get_latest_tags_diff(self, branch="master"):
        """
        Gets the diff between the two most recent tags in the repository.
        """
        [tag1, tag2] = self.get_recent_two_tags()
        return self.get_diff_between_tags(tag1, tag2, branch)

if __name__ == '__main__':
    token = "<github_token>"
    repo_name = "devx-wing/ucl-provider"
    base_url = "https://github.wdf.sap.corp/api/v3"
    user_name = "<user_name>"
    main_repo_branch = "master"
    github_settings = GitHubSettings(user_name, token, repo_name, base_url)
    scanner = GitHubScanner(user_name, token, repo_name, base_url)
    [tag1, tag2] = scanner.get_recent_two_tags()
    repo_path = scanner.get_diff_between_tags(tag1, tag2, main_repo_branch)
    print(repo_path)
