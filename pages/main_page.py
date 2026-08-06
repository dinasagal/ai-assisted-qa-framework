from __future__ import annotations

import allure

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class MainPage(BasePage):
    """GitHub main page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        # Header
        self.profile_menu = page.locator("button[data-login]")
        self.sign_out_button = page.get_by_role("link", name="Sign out")

        # Repositories
        self.repositories_tab = page.get_by_role("link", name="Repositories")

    @allure.step("Open GitHub main page")
    def open(self) -> None:
        """Open the GitHub home page."""
        self.page.goto(f"{self.base_url}/")

    @allure.step("Click on Repositories tab")
    def click_repositories(self) -> None:
        """Navigate to the user's repositories page."""
        self.repositories_tab.click()

    @allure.step("Open repository {repository_name}")
    def open_repository(self, repository_name: str) -> None:
        """Open a repository from the repositories list."""
        self.page.get_by_role("link", name=repository_name).click()

    @allure.step("Log out from GitHub")
    def logout(self) -> None:
        """Log out from GitHub."""
        self.click(self.profile_menu)
        self.click(self.sign_out_button)

        # self.sign_out_button.click()

    @allure.step("Verify repository {repository_name} exists")
    def verify_repository_exists(self, repository_name: str) -> None:
        """Verify that a repository is displayed."""
        expect(
            self.page.get_by_role("link", name=repository_name)
        ).to_be_visible()

    @allure.step("Verify user is logged in")
    def verify_logged_in(self) -> None:
        """Verify that the user is logged in."""
        expect(self.profile_menu).to_be_visible()

    @allure.step("Verify user is logged out")
    def verify_logged_out(self) -> None:
        """Verify that the user is logged out."""
        expect(self.page.get_by_role("link", name="Sign in")).to_be_visible()