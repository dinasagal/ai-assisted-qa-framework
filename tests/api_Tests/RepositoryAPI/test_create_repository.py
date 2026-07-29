import uuid
import allure
import json
import pytest
from api.api_client import ApiClient
from config.settings import GITHUB_API, GITHUB_USERNAME
from tests.api_Tests.conftest import delete_repository

OWNER = GITHUB_USERNAME

def _repo_name() -> str:
    return f"automation-{uuid.uuid4().hex[:8]}"

def _assert_repository_response(response, expected_name, *, expected_private, expected_description=None):
    assert response.status_code == 201

    body = response.json()
    assert body["name"] == expected_name
    assert body["private"] is expected_private
    assert body["owner"]["login"] == OWNER
    assert body["full_name"] == f"{OWNER}/{expected_name}"

    if expected_description is not None:
        assert body["description"] == expected_description

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
def test_create_repository_visibility(github_api, delete_repository, private, title):
    allure.dynamic.title(title)

    repo_name = _repo_name()
    delete_repository.append(repo_name)

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
def test_create_repository_with_description(github_api, delete_repository):
    repo_name = _repo_name()
    delete_repository.append(repo_name)
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
def test_create_repository_with_duplicate_name(github_api, delete_repository):
    repo_name = _repo_name()
    delete_repository.append(repo_name)

    with allure.step("Create repository"):
        response1 = github_api.create_repository(repo_name, private=True)
        _assert_repository_response(
            response1,
            repo_name,
            expected_private=True,
        )

    with allure.step("Attempt to create repository with duplicate name"):
        response2 = github_api.create_repository(repo_name, private=True)
        assert response2.status_code == 422
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
        assert response.status_code == 422
        body = response.json()
        assert "errors" in body
        assert any(error.get("message") == "name can't be blank" for error in body["errors"])

        allure.attach(
            json.dumps(body, indent=2),
            name="Response Body for Repository Without Name",
            attachment_type=allure.attachment_type.JSON,
        )
@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository with invalid characters in name")
def test_create_repository_with_invalid_characters(github_api):
    invalid_repo_name = "invalid/repo?name"
    with allure.step("Attempt to create repository with invalid characters in name"):
        response = github_api.create_repository(invalid_repo_name, private=True)
        assert response.status_code == 422
        body = response.json()
        assert "errors" in body
        assert any(error.get("message") == "name is invalid" for error in body["errors"])

        allure.attach(
            json.dumps(body, indent=2),
            name="Response Body for Repository With Invalid Characters",
            attachment_type=allure.attachment_type.JSON,
        )
@allure.epic("Repository API")
@allure.feature("Create Repository")
@allure.title("Create repository using invalid token")
def test_create_repository_with_invalid_token(github_api, delete_repository):
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


        assert response.status_code == 401
        body = response.json()
        allure.attach(
                    json.dumps(body, indent=2),
                    name="Response Body for Repository With Invalid Token",
                    attachment_type=allure.attachment_type.JSON,
                )
