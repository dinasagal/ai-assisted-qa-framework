import pytest

from pages.login_page import LoginPage
from api.github_api import GithubApi


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def github_api():
    return GithubApi()