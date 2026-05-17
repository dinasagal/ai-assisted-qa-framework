from __future__ import annotations

import pytest
import allure
from playwright.sync_api import Page

from flows.auth_flows import login_as_admin
from flows.project_flows import create_project
from pages.projects_page import ProjectsPage


@allure.epic("Project Management")
@allure.feature("Projects")
class TestProjects:

    @pytest.fixture(autouse=True)
    def _login(self, page: Page, base_url: str) -> None:
        """Ensure we are logged in before each test in this class."""
        login_as_admin(page, base_url)

    @allure.story("View projects")
    @allure.title("Projects list page is accessible after login")
    def test_projects_page_accessible(self, page: Page, base_url: str) -> None:
        projects_page = ProjectsPage(page, base_url)
        projects_page.open()
        projects_page.expect_visible(projects_page.project_list.first)

    @allure.story("Create project")
    @allure.title("Admin can create a new project")
    def test_create_project(self, page: Page, base_url: str) -> None:
        project_name = "Test Project QA"
        projects_page = create_project(page, base_url, project_name)
        projects_page.expect_project_visible(project_name)
