from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class WorkPackagesPage(BasePage):
    """Page object for a project's work packages page.

    Placeholder implementation created to satisfy the import required by
    flows/project_flows.py. Selectors/actions are not yet implemented.
    """

    def __init__(self, page: Page, base_url: str, project_id: str) -> None:
        super().__init__(page, base_url)
        self.project_id = project_id

    def open(self) -> None:
        self.navigate(f"projects/{self.project_id}/work_packages")

    def create_work_package(self, subject: str) -> None:
        raise NotImplementedError("WorkPackagesPage.create_work_package is not implemented yet.")
