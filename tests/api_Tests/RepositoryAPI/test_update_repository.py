import time
import uuid
import allure
import pytest
from config.settings import GITHUB_USERNAME
from flows.api.api_flowes import attach_response
from utils.assertions_api import assert_json_value, assert_status_code, assert_header_exists

OWNER = GITHUB_USERNAME


def _repo_name() -> str:
    return f"automation-{uuid.uuid4().hex[:8]}"


def _update_repository_with_retry(github_api, owner, repo, retries=5, delay=1.5, **kwargs):
    """GitHub briefly rejects update requests made shortly after a repository
    is created (or after a prior update) with a transient 422 error while an
    internal repository operation finishes. The exact message varies by
    field (e.g. name, visibility, archived), so retry on any 422 with a
    short backoff until the operation succeeds or a different response is
    returned."""
    response = github_api.update_repository(owner, repo, **kwargs)
    for _ in range(retries):
        if response.status_code != 422:
            return response
        time.sleep(delay)
        response = github_api.update_repository(owner, repo, **kwargs)
    return response


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository name with valid data")
def test_update_repository_name_with_valid_data(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    new_name = _repo_name()

    with allure.step("Update repository name"):
        response = _update_repository_with_retry(github_api, OWNER, repo_name, name=new_name)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "name", new_name)
        assert_json_value(body, "full_name", f"{OWNER}/{new_name}")
        attach_response(body)

    # The repository now lives under its new name; track that name for cleanup.
    created_repositories.remove(repo_name)
    created_repositories.append(new_name)

    with allure.step("Verify renamed repository is retrievable"):
        get_response = github_api.get_repository(OWNER, new_name)
        assert_status_code(get_response.status_code, 200)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository description with valid data")
def test_update_repository_description_with_valid_data(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    new_description = "Updated description via automation"

    with allure.step("Update repository description"):
        response = github_api.update_repository(OWNER, repo_name, description=new_description)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "description", new_description)
        attach_response(body)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository homepage with a valid URL")
def test_update_repository_homepage_with_a_valid_url(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    new_homepage = "https://example.com"

    with allure.step("Update repository homepage"):
        response = github_api.update_repository(OWNER, repo_name, homepage=new_homepage)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "homepage", new_homepage)
        attach_response(body)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository visibility from public to private")
def test_update_repository_visibility_from_public_to_private(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create public repository"):
        create_response = github_api.create_repository(repo_name, private=False)
        assert_status_code(create_response.status_code, 201)

    with allure.step("Update repository visibility to private"):
        response = _update_repository_with_retry(github_api, OWNER, repo_name, private=True)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "private", True)
        assert_json_value(body, "visibility", "private")
        attach_response(body)

    with allure.step("Verify repository is private"):
        get_response = github_api.get_repository(OWNER, repo_name)
        assert_status_code(get_response.status_code, 200)
        assert_json_value(get_response.json(), "private", True)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update multiple repository settings in a single request")
def test_update_multiple_repository_settings_in_a_single_request(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    new_description = "Multi-field update"

    with allure.step("Update multiple repository settings"):
        response = github_api.update_repository(
            OWNER,
            repo_name,
            description=new_description,
            has_issues=False,
            has_wiki=False,
        )

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "description", new_description)
        assert_json_value(body, "has_issues", False)
        assert_json_value(body, "has_wiki", False)
        attach_response(body)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("positive")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Archive a repository")
def test_archive_a_repository(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    with allure.step("Archive repository"):
        response = _update_repository_with_retry(github_api, OWNER, repo_name, archived=True)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "archived", True)
        attach_response(body)

    with allure.step("Verify repository is archived"):
        get_response = github_api.get_repository(OWNER, repo_name)
        assert_json_value(get_response.json(), "archived", True)

    with allure.step("Unarchive repository (clean test)"):
        unarchive_response = github_api.update_repository(OWNER, repo_name, archived=False)
        assert_status_code(unarchive_response.status_code, 200)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("boundary")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository with empty description")
def test_update_repository_with_empty_description(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository with a non-empty description"):
        create_response = github_api.create_repository(repo_name, description="Non-empty description")
        assert_status_code(create_response.status_code, 201)

    with allure.step("Update repository with empty description"):
        response = github_api.update_repository(OWNER, repo_name, description="")

    with allure.step("Validate response"):
        # GitHub normalizes an empty-string description to null rather than
        # preserving the empty string.
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "description", None)
        attach_response(body)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("negative")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update non-existing repository")
def test_update_non_existing_repository(github_api):
    non_existent_repo = f"non-existent-{uuid.uuid4().hex[:8]}"

    with allure.step("Attempt to update non-existing repository"):
        response = github_api.update_repository(OWNER, non_existent_repo, description="test")

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 404)
        attach_response(response.json())


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("negative")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository with invalid owner")
def test_update_repository_with_invalid_owner(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    invalid_owner = f"non-existent-owner-{uuid.uuid4().hex[:8]}"

    with allure.step("Attempt to update repository with invalid owner"):
        response = github_api.update_repository(invalid_owner, repo_name, description="test")

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 404)
        attach_response(response.json())


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("validation")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository with invalid visibility value")
def test_update_repository_with_invalid_visibility_value(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    with allure.step("Attempt to update repository with invalid visibility value"):
        response = github_api.update_repository(OWNER, repo_name, visibility="invalid-value")

    with allure.step("Validate response"):
        # GitHub silently ignores an unrecognized visibility value instead of
        # rejecting it; the repository's visibility remains unchanged.
        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_json_value(body, "visibility", "public")
        attach_response(body)


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("authorization")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository visibility as a non-owner when organization restricts visibility changes")
def test_update_repository_visibility_as_non_owner_when_org_restricts_visibility_changes(
    org_repository, org_member_github_api
):
    org, repo_name = org_repository

    with allure.step("Attempt to change repository visibility as a non-owner org member"):
        response = org_member_github_api.update_repository(org, repo_name, private=True)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 422)
        attach_response(response.json())


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("authorization")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update repository without sufficient permissions")
def test_update_repository_without_sufficient_permissions(github_api, created_repositories, low_privilege_github_api):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(repo_name)
        assert_status_code(create_response.status_code, 201)

    with allure.step("Attempt to update repository using a low-privilege token"):
        response = low_privilege_github_api.update_repository(OWNER, repo_name, description="test")

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 403)
        attach_response(response.json())


@allure.epic("Repository API")
@allure.feature("Update Repository")
@allure.tag("error")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.regression
@allure.title("Update a repository that has been renamed or moved")
def test_update_a_repository_that_has_been_renamed_or_moved(github_api, created_repositories):
    old_name = _repo_name()
    created_repositories.append(old_name)

    with allure.step("Create repository"):
        create_response = github_api.create_repository(old_name)
        assert_status_code(create_response.status_code, 201)

    new_name = _repo_name()

    with allure.step("Rename repository"):
        rename_response = _update_repository_with_retry(github_api, OWNER, old_name, name=new_name)
        assert_status_code(rename_response.status_code, 200)

    created_repositories.remove(old_name)
    created_repositories.append(new_name)

    with allure.step("Attempt to update repository using its former name"):
        response = github_api.update_repository(
            OWNER, old_name, description="test", allow_redirects=False
        )

    with allure.step("Validate response"):
        assert_status_code(response.status_code, 307)
        assert_header_exists(response.headers, "Location")
