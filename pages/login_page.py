from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the github login page (/login)."""

    PATH = "login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.username_input = page.locator("#login_field")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']:has-text('Sign in'), input[type='submit']").last
        self.error_message = page.locator("#js-flash-container")

    def open(self) -> "LoginPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Expect login button to be visible")
    def expect_login_btn_visible(self) -> None:
        """Expect the login button to be visible."""
        self.expect_visible(self.login_button)
  

    @allure.step("Log in as {username}")
    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    @allure.step("Log in as {username}")
    def login_with_invalid_username(self, username: str) -> None:
        self.fill(self.username_input, username)
        assert self.password_input.is_disabled()

    @allure.step("Expect login error message")
    def expect_login_error(self) -> None:
        self.expect_visible(self.error_message)

    @allure.step("Expect successful login (redirected away from /login to https://github.com/)")
    def expect_logged_in(self) -> None:
        #github_url = self.base_url + '/'
        self.expect_url("")  # Expect the base URL after successful login
