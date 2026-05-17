from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.projects_page import ProjectsPage
from pages.work_packages_page import WorkPackagesPage


@allure.step("Create project named '{name}'")
def create_project(page: Page, base_url: str, name: str) -> ProjectsPage:
    """Navigate to projects list and create a new project."""
    projects_page = ProjectsPage(page, base_url)
    projects_page.open()
    projects_page.create_project(name)
    return projects_page


@allure.step("Create work package '{subject}' in project '{project_id}'")
def create_work_package(
    page: Page, base_url: str, project_id: str, subject: str
) -> WorkPackagesPage:
    """Navigate to a project's work packages and create a new one."""
    wp_page = WorkPackagesPage(page, base_url, project_id)
    wp_page.open()
    wp_page.create_work_package(subject)
    return wp_page
