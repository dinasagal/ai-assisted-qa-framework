from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProjectsPage(BasePage):
    """Page object for the projects list page.

    Placeholder implementation created to satisfy the import required by
    flows/project_flows.py. Selectors/actions are not yet implemented.
    """

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def open(self) -> None:
        self.navigate("projects")

    def create_project(self, name: str) -> None:
        raise NotImplementedError("ProjectsPage.create_project is not implemented yet.")
