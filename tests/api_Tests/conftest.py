import time
import uuid

import pytest
import allure

from api.github_api import GithubApi
from config.settings import (
    GITHUB_USERNAME,
    GITHUB_LOW_PRIVILEGE_TOKEN,
    GITHUB_ORG,
    GITHUB_ORG_MEMBER_TOKEN,
)

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
            # A repository that was just created/updated can briefly reject
            # further operations (409/422) while GitHub finishes an internal
            # repository operation. Retry with a short backoff before failing.
            for _ in range(5):
                if response.status_code == 204:
                    break
                time.sleep(1.5)
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


@pytest.fixture(scope="function")
def low_privilege_github_api():
    """GithubApi client authenticated with a token that lacks Administration
    write permission on the target repository. Requires
    GITHUB_LOW_PRIVILEGE_TOKEN to be configured; skips otherwise."""
    if not GITHUB_LOW_PRIVILEGE_TOKEN:
        pytest.skip("GITHUB_LOW_PRIVILEGE_TOKEN is not configured")
    return GithubApi(token=GITHUB_LOW_PRIVILEGE_TOKEN)


@pytest.fixture(scope="function")
def org_member_github_api():
    """GithubApi client authenticated as a non-owner member of GITHUB_ORG.
    Requires GITHUB_ORG_MEMBER_TOKEN to be configured; skips otherwise."""
    if not GITHUB_ORG_MEMBER_TOKEN:
        pytest.skip("GITHUB_ORG_MEMBER_TOKEN is not configured")
    return GithubApi(token=GITHUB_ORG_MEMBER_TOKEN)


@pytest.fixture(scope="function")
def org_repository(github_api):
    """Creates an organization-owned repository under GITHUB_ORG. Assumes the
    organization already restricts repository visibility changes to
    organization owners. Requires GITHUB_ORG to be configured; skips
    otherwise."""
    if not GITHUB_ORG:
        pytest.skip("GITHUB_ORG is not configured")

    repo_name = f"automation-{uuid.uuid4().hex[:8]}"
    response = github_api.create_org_repository(GITHUB_ORG, repo_name, private=False)
    assert response.status_code == 201

    yield GITHUB_ORG, repo_name

    github_api.delete_repository(GITHUB_ORG, repo_name)
