from __future__ import annotations

import allure
from playwright.sync_api import Page

from config.settings import ADMIN_USER, ADMIN_PASSWORD
from pages.login_page import LoginPage


@allure.step("Perform admin login")
def login_as_admin(page: Page, base_url: str) -> None:
    """Log in with admin credentials and assert successful authentication."""
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login(ADMIN_USER, ADMIN_PASSWORD)
    login_page.expect_logged_in()


@allure.step("Log in as {username}")
def login_as(page: Page, base_url: str, username: str, password: str) -> None:
    """Log in with arbitrary credentials."""
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login(username, password)
