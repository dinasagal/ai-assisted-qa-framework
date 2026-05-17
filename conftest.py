from __future__ import annotations

import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.settings import BASE_URL, HEADLESS, SLOW_MO, DEFAULT_TIMEOUT


# ------------------------------------------------------------------ #
# Browser / context / page fixtures
# ------------------------------------------------------------------ #

@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser for the entire test session."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    """Fresh browser context (isolated cookies/storage) per test."""
    ctx = browser_instance.new_context(base_url=BASE_URL)
    ctx.set_default_timeout(DEFAULT_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """New page per test."""
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


# ------------------------------------------------------------------ #
# Allure: attach screenshot on test failure
# ------------------------------------------------------------------ #

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture is not None:
            allure.attach(
                page_fixture.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
