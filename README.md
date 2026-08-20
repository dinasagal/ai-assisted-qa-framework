# ai-assisted-qa-framework

AI-assisted QA framework for UI and API testing:

- **Playwright** — browser automation
- **Pytest** — test execution
- **Allure** — rich HTML reporting
- **Page Object Model (POM)** — maintainable page layer
- **Reusable flows** — composable multi-step test helpers

---

## Project structure

├── api/
│ ├── api_client.py 
│ └── github_api.py 
├── config/
│ └── settings.py 
├── pages/
│ ├── base_page.py 
│ ├── login_page.py
│ ├── logout_page.py
│ └── main_page.py
├── flows/
│ ├── auth_flows.py
│ ├── project_flows.py 
│ └── api/
│ └── api_flowes.py 
├── utils/
│ └── assertions_api.py 
├── ai_agent/
│ ├── generated_test_plans.txt
│ └── test_plan_generator.md
├── tests/
│ ├── ui/
│ │ ├── conftest.py
│ │ └── test_login.py
│ └── api_Tests/
│ ├── conftest.py
│ ├── test_crud_repository.py
│ └── RepositoryAPI/
│ ├── test_create_repository.py
│ └── test_get_repository.py
├── conftest.py 
├── pytest.ini
├── requirements.txt
└── .env.example
```


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
