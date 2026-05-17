from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from .base_page import BasePage


class WorkPackagesPage(BasePage):
    """Page object for the OpenProject work-packages view (/projects/{id}/work_packages)."""

    def __init__(self, page: Page, base_url: str, project_id: str) -> None:
        super().__init__(page, base_url)
        self.project_id = project_id
        self.path = f"projects/{project_id}/work_packages"
        self.create_button = page.get_by_role("button", name="Create")
        self.subject_input = page.locator("#wp-new-inline-edit--field-subject")
        self.save_button = page.locator(".wp-inline-create--save-button")
        self.work_package_rows = page.locator(".wp-table--row")

    def open(self) -> "WorkPackagesPage":
        self.navigate(self.path)
        return self

    @allure.step("Create work package with subject '{subject}'")
    def create_work_package(self, subject: str) -> None:
        self.click(self.create_button)
        self.fill(self.subject_input, subject)
        self.click(self.save_button)

    def expect_work_package_visible(self, subject: str) -> None:
        with allure.step(f"Expect work package '{subject}' in list"):
            expect(self.page.get_by_text(subject)).to_be_visible()
