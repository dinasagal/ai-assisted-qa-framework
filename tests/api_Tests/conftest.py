import pytest
import allure

from api.github_api import GithubApi
from config.settings import GITHUB_USERNAME

owner = GITHUB_USERNAME
@pytest.fixture(scope="function")
def github_api():
    """Fixture to provide an instance of GithubApi."""
    return GithubApi()

@pytest.fixture(scope="function")
def delete_repository(github_api):
    """Fixture to delete a repository after test execution."""
    created_repos = []

    yield created_repos

    with allure.step("Delete repository"):
        for repo in created_repos:
            response = github_api.delete_repository(owner, repo)
            assert response.status_code == 204
            allure.attach(
                f"Deleted repository: {repo}",
                name="Repository Deletion",
                attachment_type=allure.attachment_type.TEXT,
            )