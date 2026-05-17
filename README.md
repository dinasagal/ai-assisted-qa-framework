# ai-assisted-qa-framework

AI-assisted QA framework for the **OpenProject** SaaS application, built with:

- **Playwright** — browser automation
- **Pytest** — test execution
- **Allure** — rich HTML reporting
- **Page Object Model (POM)** — maintainable page layer
- **Reusable flows** — composable multi-step test helpers

---

## Project structure

```
├── config/
│   └── settings.py          # Base URL, credentials, timeouts (env-configurable)
├── pages/
│   ├── base_page.py          # BasePage with shared Playwright helpers
│   ├── login_page.py
│   ├── projects_page.py
│   └── work_packages_page.py
├── flows/
│   ├── auth_flows.py         # login_as_admin(), login_as()
│   └── project_flows.py      # create_project(), create_work_package()
├── tests/
│   ├── test_login.py
│   └── test_projects.py
├── conftest.py               # browser/context/page fixtures + failure screenshots
├── pytest.ini
├── requirements.txt
└── .env.example
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium

# 4. Configure the target environment
cp .env.example .env
# Edit .env with your OpenProject URL and credentials
```

---

## Running tests

```bash
# Run all tests (headless, results written to allure-results/)
pytest

# Run a specific file
pytest tests/test_login.py

# Run headed (visible browser)
HEADLESS=false pytest

# Run against a different environment
BASE_URL=https://your-openproject.example.com pytest
```

---

## Allure reports

```bash
# Generate and open the HTML report
allure serve allure-results
```

> Requires the [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) to be installed.
