from __future__ import annotations

import pytest
import allure
from playwright.sync_api import Page

from pages.logout_page import LogoutPage
from pages.login_page import LoginPage
from config.settings import ADMIN_USER, ADMIN_PASSWORD
from pages.main_page import MainPage


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:

    @allure.story("Successful login")
    @allure.title("Login page is accessible at /login")
    def test_login_page_accessible(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.expect_login_btn_visible()

    @allure.story("Successful login")
    @allure.title("Admin can log in with valid credentials")
    def test_login_success(self, page: Page, base_url: str) -> None:
        with allure.step("Log in with user name and password"):
            login_page = LoginPage(page, base_url)
            login_page.open()
            login_page.login(ADMIN_USER, ADMIN_PASSWORD)
            login_page.expect_logged_in()
        with allure.step("Verify user is logged in and user name is correct"):
            main_page = MainPage(page, base_url)
            main_page.verify_logged_in()
            main_page.verify_user_name()

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

    @allure.story("Successful login")
    @allure.title("Admin can log in with valid credentials")
    def test_login_success2(self, page: Page, base_url: str) -> None:
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.login(ADMIN_USER, ADMIN_PASSWORD)
        login_page.expect_logged_in()

             
    @allure.story("Successful login and logout")
    @allure.title("Admin can log in and log out successfully")
    def test_login_and_logout(self, page: Page, base_url: str) -> None:
        with allure.step("Log in as admin"):
            login_page = LoginPage(page, base_url)
            login_page.open()
            login_page.login(ADMIN_USER, ADMIN_PASSWORD)
            login_page.expect_logged_in()
        with allure.step("Log out via main page"):
            main_page = MainPage(page, base_url)
            main_page.verify_logged_in()
            main_page.logout()
        with allure.step("Confirm logout on logout page"):
            logout_page = LogoutPage(page, base_url)
            logout_page.confirm_logout()
            logout_page.verify_logged_out()
        