from api.api_client import ApiClient
from config.settings import GITHUB_API, GITHUB_TOKEN


class GithubApi:
    
    def __init__(self, token=None):

        headers = {
            "Authorization": f"Bearer {token or GITHUB_TOKEN}",
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

    def create_org_repository(
        self,
        org,
        repo_name,
        private=False,
        description=None,
        **kwargs,
    ):
        """Create a repository owned by an organization."""

        body = {
            "name": repo_name,
            "private": private,
            "description": description,
            **kwargs,
        }

        return self.client.post(
            f"/orgs/{org}/repos",
            body
        )

    def get_repository(self, owner, repo):
        """Get a repository by owner and repo name."""

        return self.client.get(f"/repos/{owner}/{repo}")
    
    def update_repository(self, owner, repo, description=None, allow_redirects=True, **kwargs):
        """Update a repository's metadata/settings.

        `description` maps to the `description` field. Additional fields
        (e.g. name, private, visibility, homepage, archived) can be passed
        as keyword arguments and are merged into the request body.
        """

        body = {}
        if description is not None:
            body["description"] = description
        body.update(kwargs)

        return self.client.patch(
            f"/repos/{owner}/{repo}",
            body,
            allow_redirects=allow_redirects,
        )
    
    def delete_repository(self, owner, repo):

        return self.client.delete(
            f"/repos/{owner}/{repo}"
        )
