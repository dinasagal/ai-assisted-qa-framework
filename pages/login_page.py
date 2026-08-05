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

    @allure.step("Log in as {username}")
    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    @allure.step("Log in as {username}")
    def login_with_invalid_username(self, username: str) -> None:
        self.fill(self.username_input, username)
        assert self.password_input.is_disabled()

    def expect_login_error(self) -> None:
        with allure.step("Expect login error message"):
            expect(self.error_message).to_be_visible()

    def expect_logged_in(self) -> None:
        with allure.step("Expect successful login (redirected away from /login)"):
            expect(self.page).not_to_have_url(f"{self.base_url}/{self.PATH}")
