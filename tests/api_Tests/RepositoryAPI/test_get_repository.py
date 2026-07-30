import allure
import json
import pytest
from config.settings import GITHUB_USERNAME
from flows.api.api_flowes import attach_response



@allure.epic("Repository API")
@allure.feature("Get Repository")
class TestGetRepository:

    def _get_repository(self, github_api, repo_name, expected_status_code=200):
        with allure.step("Get repository"):
            response = github_api.get_repository(GITHUB_USERNAME, repo_name)
            allure.attach(
                f"GET /repos/{GITHUB_USERNAME}/{repo_name}",
                name="Request",
                attachment_type=allure.attachment_type.TEXT,
            )
        with allure.step(f"Validate response status_code == {expected_status_code}"):
            assert response.status_code == expected_status_code
        return response.json()


    @allure.title("Get repository by owner and repo name")
    def test_get_repository(self, github_api, shared_repository):
        """Test to get a repository by owner and repo name."""
        repo_name = shared_repository
        owner = GITHUB_USERNAME

        response_data = self._get_repository(github_api, repo_name)
        with allure.step("Validate repository details"):
            assert response_data["name"] == repo_name
            assert response_data["owner"]["login"] == owner
            attach_response(response_data)

    @allure.title("Verify repository description")
    def test_verify_description(self, github_api, shared_repository):
        """Test to verify the description of a repository."""
        repo_name = shared_repository

        response_data = self._get_repository(github_api, repo_name)

        with allure.step("Validate repository description"):
            assert response_data["description"] == "Repository for class tests"
            attach_response(response_data)

    @allure.title("Verify repository visibility")
    def test_verify_visibility(self, github_api, shared_repository):
        """Test to verify the visibility of a repository."""
        repo_name = shared_repository

        response_data = self._get_repository(github_api, repo_name)
        with allure.step("Validate repository visibility is public"):
            assert response_data["private"] is False
            assert response_data["visibility"] == "public"
            attach_response(response_data)

    @allure.title("Get non-existent repository")
    def test_get_non_existent_repository(self, github_api):
        """Test to get a non-existent repository."""
        non_existent_repo = "non-existent-repo"

        response_data = self._get_repository(github_api, non_existent_repo, expected_status_code=404)

        with allure.step("Validate response for non-existent repository"):
            assert response_data["message"] == "Not Found"
            attach_response(response_data)

    @allure.title("Get repository without authentication")
    def test_get_repository_without_authentication(self, github_api, shared_repository):
        """Test to get a repository without authentication."""
        repo_name = shared_repository
        owner = GITHUB_USERNAME

        # Temporarily remove the Authorization header
        original_headers = github_api.client.headers.copy()
        try:
            github_api.client.headers.pop("Authorization", None)
            with allure.step("Get repository without authentication"):
                response_data = self._get_repository(github_api, repo_name)

            with allure.step("Validate response for unauthenticated request"):
                assert response_data["name"] == repo_name
                assert response_data["owner"]["login"] == owner
                attach_response(response_data)
        finally:
            # Restore the original headers
            github_api.client.headers = original_headers