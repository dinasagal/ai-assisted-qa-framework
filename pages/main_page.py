from __future__ import annotations

import allure

from playwright.sync_api import Page, expect

from config.settings import GITHUB_USERNAME
from pages.base_page import BasePage


class MainPage(BasePage):
    """GitHub main page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        # Exact avatar trigger used by logged-in header
        self.profile_menu = page.locator(
            "button[data-login][aria-haspopup='menu']:has(img[data-testid='github-avatar'])"
        ).first

        

        # Menu action used as open-state proof
        self.sign_out_button = page.get_by_role("link", name="Sign out")

        # Repositories
        self.repositories_tab = page.get_by_role("link", name="Repositories")

        # Username heading shown inside the open user menu
        self.username_heading = page.get_by_role("heading", name=GITHUB_USERNAME)


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

    @allure.step("Open user menu")
    def open_user_menu(self) -> None:
        """Open user menu from avatar button."""
        expect(self.profile_menu).to_be_visible(timeout=10000)
        self.profile_menu.scroll_into_view_if_needed()
        self.profile_menu.click(timeout=10000)
        expect(self.sign_out_button).to_be_visible(timeout=10000)
        


    @allure.step("Log out from GitHub")
    def logout(self) -> None:
        """Log out from GitHub."""
        expect(self.sign_out_button).to_be_visible(timeout=10000)
        self.sign_out_button.click()

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
        """Verify that user menu opens and account actions are visible."""
        self.open_user_menu()
        with allure.step(f"Expect element: {self.username_heading} visible"):
            expect(self.username_heading).to_be_visible(timeout=10000)

