from __future__ import annotations

import allure

from playwright.sync_api import Page, expect

from config.settings import GITHUB_USERNAME
from pages.base_page import BasePage


class MainPage(BasePage):
    """GitHub main page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        # Header
        self.profile_menu = page.locator("button[data-login]")
        self.username_label = page.locator(f"div[title='{GITHUB_USERNAME}']")
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
        self.expect_visible(
            self.page.get_by_role("link", name=repository_name)
        )

    @allure.step("Verify user is logged in")
    def verify_logged_in(self) -> None:
        """Verify that the user is logged in."""
        self.expect_visible(self.profile_menu)

    @allure.step("Verify user name is correct")
    def verify_user_name(self) -> None:
        """Verify that the logged-in user's name is correct."""
        self.click(self.profile_menu)
        self.expect_visible(self.username_label)

