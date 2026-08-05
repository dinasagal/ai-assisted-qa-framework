from __future__ import annotations

import pytest
import allure
from playwright.sync_api import Page

from pages.login_page import LoginPage
from config.settings import ADMIN_USER, ADMIN_PASSWORD


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:

    @allure.story("Successful login")
    @allure.title("Login page is accessible at /login")
    def test_login_page_accessible(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.expect_visible(login_page.login_button)

    @allure.story("Successful login")
    @allure.title("Admin can log in with valid credentials")
    def test_login_success(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login(ADMIN_USER, ADMIN_PASSWORD)
        login_page.expect_logged_in()

    @allure.story("Failed login")
    @allure.title("Login fails with wrong password")
    def test_login_wrong_credentials(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login(ADMIN_USER, "wrong password")
        login_page.expect_login_error()

    @allure.story("Failed login")
    @allure.title("Login fails with wrong username")
    def test_login_wrong_username(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login("wrong user", ADMIN_PASSWORD)
        login_page.expect_login_error()

    @allure.story("Failed login")
    @allure.title("Login fails with invalid username")
    def test_login_invalid_username(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login_with_invalid_username("invalid_user")
        

    
