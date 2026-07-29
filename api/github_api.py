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

    def create_repository(
        self,
        repo_name,
        private=False,
        description=None,
        **kwargs,
    ):

        body = {
            "name": repo_name,
            "private": private,
            "description": description
        }

        return self.client.post(
            "/user/repos",
            body
        )
    def get_repository(self, owner, repo):
        """Get a repository by owner and repo name."""

        return self.client.get(f"/repos/{owner}/{repo}")
    
    def update_repository(self, owner, repo, new_description):

        body = {
            "description": new_description
        }

        return self.client.patch(
            f"/repos/{owner}/{repo}",
            body
        )
    
    def delete_repository(self, owner, repo):

        return self.client.delete(
            f"/repos/{owner}/{repo}"
        )
