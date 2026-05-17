from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from .base_page import BasePage


class ProjectsPage(BasePage):
    """Page object for the OpenProject projects list page (/projects)."""

    PATH = "projects"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.new_project_button = page.get_by_role("link", name="+ Project")
        self.project_name_input = page.locator("#project_name")
        self.create_project_button = page.locator("[name='commit']")
        self.project_list = page.locator(".project-name")

    def open(self) -> "ProjectsPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Create project named '{name}'")
    def create_project(self, name: str) -> None:
        self.click(self.new_project_button)
        self.fill(self.project_name_input, name)
        self.click(self.create_project_button)

    def expect_project_visible(self, name: str) -> None:
        with allure.step(f"Expect project '{name}' in list"):
            expect(self.page.get_by_text(name)).to_be_visible()
