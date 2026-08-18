import uuid
import allure
import json
import pytest
from api.api_client import ApiClient
from config.settings import GITHUB_API, GITHUB_USERNAME
from tests.api_Tests.conftest import created_repositories
from utils.assertions_api import assert_json_value, assert_status_code

OWNER = GITHUB_USERNAME

def _repo_name() -> str:
    return f"automation-{uuid.uuid4().hex[:8]}"

def _assert_repository_response(response, expected_name, *, expected_private, expected_description=None):
    assert_status_code(response.status_code, 201)

    body = response.json()
    assert_json_value(body, "name", expected_name)
    assert_json_value(body, "private", expected_private)
    assert_json_value(body, "owner.login", OWNER)
    assert_json_value(body, "full_name", f"{OWNER}/{expected_name}")

    if expected_description is not None:
        assert_json_value(body, "description", expected_description)

    allure.attach(
        json.dumps(body, indent=2),
        name="Response Body",
        attachment_type=allure.attachment_type.JSON,
    )

@allure.epic("Repository API")
@allure.feature("Create Repository")
@pytest.mark.parametrize(
    ("private", "title"),
    [
        (True, "Create private repository"),
        (False, "Create public repository"),
    ],
)
def test_create_repository_visibility(github_api, created_repositories, private, title):
    allure.dynamic.title(title)

    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        response = github_api.create_repository(repo_name, private=private)

    with allure.step("Validate repository"):
        _assert_repository_response(
            response,
            repo_name,
            expected_private=private,
        )

@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository with description")
def test_create_repository_with_description(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)
    description = "This is a test repository created via API."
    
    with allure.step("Create repository with description"):
        response = github_api.create_repository(
            repo_name,
            private=True,
            description=description
        )
        allure.attach(
            description,
            name="Repository description",
            attachment_type=allure.attachment_type.TEXT,
        )
    
    with allure.step("Validate repository"):
        _assert_repository_response(
            response,
            repo_name,
            expected_private=True,
            expected_description=description,
        )
@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository with duplicate name")
def test_create_repository_with_duplicate_name(github_api, created_repositories):
    repo_name = _repo_name()
    created_repositories.append(repo_name)

    with allure.step("Create repository"):
        response1 = github_api.create_repository(repo_name, private=True)
        _assert_repository_response(
            response1,
            repo_name,
            expected_private=True,
        )

    with allure.step("Attempt to create repository with duplicate name"):
        response2 = github_api.create_repository(repo_name, private=True)
        assert_status_code(response2.status_code, 422)
        body = response2.json()
        assert "errors" in body
        assert any(error.get("message") == "name already exists on this account" for error in body["errors"])

        allure.attach(
            json.dumps(body, indent=2),
            name="Response Body for Duplicate Repository",
            attachment_type=allure.attachment_type.JSON,
        )

@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository without name")
def test_create_repository_without_name(github_api):
    with allure.step("Attempt to create repository without name"):
        response = github_api.create_repository("", private=True)
        assert(response.status_code == 422)

    with allure.step("Validate response for repository without name"):
        body = response.json()
        allure.attach(
                json.dumps(body, indent=2),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )
        with allure.step("Verify error message"):
            assert body["message"] == "New repository name must not be blank"
            assert body["status"] == "422"

        with allure.step("Verify missing name validation error"):
            errors = body["errors"]

            assert {
                "resource": "Repository",
                "field": "name",
                "code": "missing_field",
            } in errors

        with allure.step("Verify minimum length validation error"):
            assert {
                "resource": "Repository",
                "field": "name",
                "code": "custom",
                "message": "name is too short (minimum is 1 character)",
            } in errors
        
        




@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository with invalid characters in name")
def test_create_repository_with_invalid_characters(github_api):
    invalid_repo_name = "invalid/repo?name" #invalid-repo-name
    with allure.step("Attempt to create repository with invalid characters in name"):
        response = github_api.create_repository(invalid_repo_name, private=True)
        assert_status_code(response.status_code, 201)
        with allure.step("Validate repository"):
                _assert_repository_response(
                    response,
                    "invalid-repo-name",
                    expected_private=True,
                )


@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository using invalid token")
def test_create_repository_with_invalid_token(github_api, created_repositories):
    with allure.step("Attempt to create repository using invalid token"):
        headers = {
                    "Authorization": f"Bearer {"ghpp_FsoqaLXGSvEoPNGRHz3QxzkT2su4gRdGW"}",
                    "Accept": "application/vnd.github+json"
                }
        
        client = ApiClient(
                GITHUB_API,
                headers=headers
                )

        body = {
                    "name": "test-repo-invalid-token",
                    "private": True,
                    "description": ""
                }
        
        response = client.post(
                    "/user/repos",
                    body
                )


        assert_status_code(response.status_code, 401)
        body = response.json()
        allure.attach(
                    json.dumps(body, indent=2),
                    name="Response Body for Repository With Invalid Token",
                    attachment_type=allure.attachment_type.JSON,
                )
