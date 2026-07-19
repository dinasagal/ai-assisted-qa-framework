from api.api_client import ApiClient
from config.settings import GITHUB_API, GITHUB_TOKEN


class GithubApi:

    def __init__(self):

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        self.client = ApiClient(
            GITHUB_API,
            headers=headers
        )

    def create_repository(self, repo_name):

        body = {
            "name": repo_name,
            "private": False
        }

        return self.client.post(
            "/user/repos",
            body
        )