from __future__ import annotations

import allure
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base class for all page objects. Wraps common Playwright operations."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #

    def navigate(self, path: str = "") -> None:
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    # ------------------------------------------------------------------ #
    # Interaction helpers
    # ------------------------------------------------------------------ #

    def click(self, locator: Locator) -> None:
        with allure.step(f"Click {locator}"):
            locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        with allure.step(f"Fill field with value"):
            locator.fill(value)

    def select_option(self, locator: Locator, value: str) -> None:
        with allure.step(f"Select option '{value}'"):
            locator.select_option(value)

    # ------------------------------------------------------------------ #
    # Assertions
    # ------------------------------------------------------------------ #

    def expect_url(self, path: str) -> None:
        expected = f"{self.base_url}/{path.lstrip('/')}"
        with allure.step(f"Expect URL to contain '{path}'"):
            expect(self.page).to_have_url(expected)

    def expect_visible(self, locator: Locator) -> None:
        with allure.step(f"Expect element visible"):
            expect(locator).to_be_visible()

    # ------------------------------------------------------------------ #
    # Screenshot utility
    # ------------------------------------------------------------------ #

    def attach_screenshot(self, name: str = "screenshot") -> None:
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
