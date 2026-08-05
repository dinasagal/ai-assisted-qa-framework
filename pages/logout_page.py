from __future__ import annotations
import re

import allure

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LogoutPage(BasePage):
    """GitHub logout confirmation page."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

        self.sign_out_button =  page.locator('input[type="submit"][value="Sign out"]')
        self.cancel_button = page.get_by_role("link", name="Cancel")
        self.page_title = page.get_by_role("heading", name="Sign out")
        self.login_button = page.get_by_role("link", name="Sign in")

    @allure.step("Log out from GitHub")
    def verify_logout_page_loaded(self) -> None:
        """Verify the logout confirmation page is displayed."""
        expect(self.page_title).to_be_visible()
        expect(self.sign_out_button).to_be_visible()


    @allure.step("Confirm logout")
    def confirm_logout(self) -> None:
        """Confirm logout."""
        self.sign_out_button.click()

    @allure.step("Cancel logout")
    def cancel_logout(self) -> None:
        """Cancel logout."""
        self.cancel_button.click()

    @allure.step("Verify logged out")
    def verify_logged_out(self) -> None:
        """Verify the user has been logged out."""
        expect(self.login_button).to_be_visible()