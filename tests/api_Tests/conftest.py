import uuid

import pytest
import allure

from api.github_api import GithubApi
from config.settings import GITHUB_USERNAME

owner = GITHUB_USERNAME
@pytest.fixture(scope="class")
def github_api():
    """Fixture to provide an instance of GithubApi."""
    return GithubApi()

@pytest.fixture(scope="function")
def created_repositories(github_api):
    """Fixture to track created repositories and delete them after test execution."""
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
            
@pytest.fixture(scope="class")
def shared_repository(request, github_api):
    repo_name = f"automation-{uuid.uuid4().hex[:8]}"

    response = github_api.create_repository(repo_name, False, description="Repository for class tests")
    assert response.status_code == 201

    yield repo_name

    response = github_api.delete_repository(GITHUB_USERNAME, repo_name)
    assert response.status_code == 204