# AI-Assisted QA Automation Framework

A Python-based QA automation project that combines **UI and API test automation** with an **AI-assisted workflow for test planning, test implementation, and test execution/analysis**.

The project explores a structured approach to using AI in QA:

```text
Feature
   ↓
AI Test Plan Agent
   ↓
Structured QA Test Plan
   ↓
AI Test Implementation Agent
   ↓
Runnable Automated Tests
   ↓
AI Test Execution & Analysis Agent
   ↓
Execution Report (pass/fail triage, root cause, proposed fixes)
```

## What This Project Demonstrates

* UI automation with Playwright
* API testing with Python and Pytest
* Page Object Model for UI test organization
* Reusable flows and fixtures
* API client abstraction
* Test setup and cleanup
* Allure reporting
* AI-assisted test planning
* AI-assisted test implementation
* AI-assisted test execution and failure analysis

## AI-Assisted Test Workflow

### 1. Test Plan Agent

The Test Plan Agent receives a feature or requirement and creates a structured QA test plan.

It is designed to:

* Research the relevant official GitHub API documentation
* Identify relevant positive, negative, boundary, validation, authorization, and error scenarios
* Avoid inventing undocumented API behavior
* Flag unclear behavior for clarification
* Produce a structured test plan independent of the automation framework

The generated plan is stored in:

```text
ai_agent/generated_ai_test_plans.md
```

### 2. Test Implementation Agent

The Test Implementation Agent takes an existing feature from the generated test plan and implements it inside the existing automation framework.

It:

* Reads the test plan as the source of truth
* Inspects the existing framework before implementation
* Reuses existing fixtures, API clients, helpers, and flows
* Extends framework components when required
* Adds appropriate Pytest and Allure metadata
* Separates AI-generated tests using the `ai_test` marker
* Runs `pytest --collect-only` to validate that generated tests can be collected

The goal is to move from:

**Feature → Test Plan → Automated Test Code**

while keeping the generated code consistent with the existing framework.

### 3. Test Execution & Analysis Agent

The Test Execution & Analysis Agent runs an already-implemented feature's automated tests and triages the results. It is **read-only with respect to code** — it never edits tests, framework code, or application code, and never applies a fix itself; it only investigates and proposes one.

It:

* Resolves a feature name to its test file (same convention as the Implementation Agent) and runs only that feature's tests, not the full suite
* Collects execution evidence per test: outcome, HTTP status/response body, stack trace, and Allure data
* Investigates every failure (request/response, docs, framework behavior, test data, git history) before classifying — never classifies from the assertion message alone
* Classifies each failure into exactly one category: `BUG_IN_TEST`, `BUG_IN_FEATURE`, `ENVIRONMENT_ISSUE`, `TEST_DATA_ISSUE`, `INFRASTRUCTURE_ISSUE`, or `REQUIRES_CLARIFICATION`
* For `BUG_IN_TEST`, traces the problematic change via `git log`/`git blame` and reports commit evidence (no invented PR/branch references) plus a recommended (not applied) fix
* For `BUG_IN_FEATURE`, produces a defect report (expected/actual/repro/evidence/severity) instead of altering the test
* Builds a traceability table: Test Plan entry → Implemented Test → Execution Result → Classification
* Writes a full report per run to `ai_agent/generated_execution_reports/<feature>_execution_report_<timestamp>.md` (git-ignored, local artifact)

The goal is to move from:

**Automated Test Code → Execution → Classified, Actionable Results**

closing the loop from requirement to a triaged, explainable test run.

## Framework Architecture

```text
ai_agent/
│
├── Test Plan Agent
│       ↓
│   generated_ai_test_plans.md
│       ↓
├── Test Implementation Agent
│       ↓
│       ├── API Tests
│       ├── API Client
│       ├── Fixtures
│       └── Assertion Helpers
│       ↓
└── Test Execution & Analysis Agent
        ↓
        generated_execution_reports/<feature>_execution_report_<timestamp>.md


UI Tests
    ↓
Page Objects
    ↓
Reusable Flows
    ↓
Playwright


API Tests
    ↓
GitHub API Wrapper
    ↓
Reusable Fixtures
    ↓
Assertion Helpers
```

## Tech Stack

* **Python**
* **Pytest**
* **Playwright**
* **GitHub REST API**
* **Allure**
* **python-dotenv**

## Example API Test Coverage

The project currently includes GitHub Repository API testing.

Examples include:

* Create a repository
* Retrieve and verify a repository
* Update repository data
* Verify the update
* Delete the repository
* Verify deletion

Tests use reusable API methods and fixtures for setup and cleanup rather than placing all request logic directly inside test cases.

## Project Structure

```text
ai-assisted-qa-framework/
│
├── ai_agent/        # AI test planning and implementation agents
├── api/             # API client and GitHub API wrapper
├── config/          # Environment configuration
├── flows/           # Reusable UI and API flows
├── pages/           # Playwright Page Objects
├── tests/
│   ├── ui/          # UI tests
│   └── api_Tests/   # API tests
├── utils/           # Reusable assertion helpers
│
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Running the Project

```bash
git clone https://github.com/dinasagal/ai-assisted-qa-framework.git
cd ai-assisted-qa-framework

python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

Create your environment configuration:

```bash
cp .env.example .env
```

Run the tests:

```bash
pytest
```

Run AI-generated API tests:

```bash
pytest -m ai_test
```

View Allure results:

```bash
allure serve allure-results
```

## About This Project

I built this project to explore how AI can support the QA automation lifecycle without separating AI-generated tests from good automation practices.

The focus is on combining **QA test design, reusable automation architecture, and AI-assisted implementation** in a single workflow.

## Author

**Dina Rozenblat**
QA Automation Engineer

Python • Playwright • Pytest • API Testing • Allure • AI-Assisted QA
