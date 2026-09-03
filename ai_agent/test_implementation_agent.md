# GitHub API Test Implementation Agent

## Role

Act as a senior SDET (Software Development Engineer in Test) specializing in Python, pytest, and API test automation.

Your **only responsibility** is to take an existing QA test plan feature section from `ai_agent/generated_ai_test_plans.md` and implement it as real, runnable automated tests inside this repository's existing test automation framework.

You do **NOT** invent new test scenarios. The test plan is the source of truth for *what* to test.

You do **NOT** implement UI tests. This skill covers **API tests only** (`tests/api_Tests/`).

You do **NOT** silently skip test plan entries — every test listed under the requested feature must either be implemented or explicitly reported as not implemented (see "Handling Clarification-Flagged Tests").

---

# Objective

When given a feature name to implement:

1. Read `ai_agent/generated_ai_test_plans.md` and locate the `# FEATURE:` section matching the requested feature name (case-insensitive, ignoring extra whitespace).
2. If the feature section is not found, report this to the user and stop.
3. Parse the feature's `Description`, `Plan type`, `Documentation`, `Test List`, `Prepare`, each `Test N` block (`Type`, `Prepare test`, `Steps`, `Expected`, `Clean test`), and `Clean`.
4. Identify any test whose `Expected` explicitly states the behavior "requires clarification" (undocumented behavior flagged by the test plan generator).
5. Inspect the existing test automation framework to determine reusable fixtures, helpers, and API client methods.
6. Implement every test in the feature (except clarification-flagged tests) as pytest test functions/methods using the framework conventions below.
7. Extend framework code (API client, fixtures, helpers) when the test plan requires capabilities that do not exist yet.
8. Validate the generated/updated test file(s) by running `pytest --collect-only` against them.
9. Report a summary to the user, including any clarification-flagged tests that were **not** implemented.

---

# Source of Truth

Use the following sources in this order:

1. The feature section in `ai_agent/generated_ai_test_plans.md`.
2. Existing test files for the same feature group (e.g. `tests/api_Tests/RepositoryAPI/`) for style and structure conventions.
3. Existing framework code: `api/github_api.py`, `api/api_client.py`, `utils/assertions_api.py`, `flows/api/api_flowes.py`, `tests/api_Tests/conftest.py`.
4. `config/settings.py` for environment/config values (e.g. `GITHUB_API`, `GITHUB_USERNAME`, `GITHUB_TOKEN`).

Do not invent test steps or expected results beyond what the test plan specifies.

Do not "fill in" behavior for clarification-flagged tests — see the dedicated section below.

---

# File Placement Rules

Tests are organized by feature group under `tests/api_Tests/`:

* Place tests in `tests/api_Tests/<FeatureGroup>API/test_<feature>.py`, matching the existing convention (e.g. `tests/api_Tests/RepositoryAPI/test_create_repository.py`, `tests/api_Tests/RepositoryAPI/test_get_repository.py`).
* Derive `<feature>` from the FEATURE name in snake_case (e.g. "Update Repository" → `test_update_repository.py`).
* If a test file for the feature already exists:
  * Do not duplicate existing tests.
  * Match that file's existing style exactly (see "Test Structure Style" below).
  * Append new tests only for scenarios not already covered.
* If no test file exists for the feature yet:
  * Create a new file under the appropriate `<FeatureGroup>API/` directory (create the directory if the feature group doesn't exist yet).
  * Default to **function-based** style (no test class) for brand-new files.

---

# Test Structure Style

This framework uses two existing styles. Choose based on the rule above:

### Function-based (default for new files)

```python
import allure
import json
import pytest
from api.api_client import ApiClient
from config.settings import GITHUB_API, GITHUB_USERNAME
from utils.assertions_api import assert_json_value, assert_status_code

OWNER = GITHUB_USERNAME


@allure.epic("Repository API")
@allure.feature("<Feature Name>")
@pytest.mark.api
@pytest.mark.ai_test
@pytest.mark.<sanity|smoke|regression>
@allure.title("<Test title from plan>")
def test_<snake_case_title>(github_api, created_repositories):
    with allure.step("<step description>"):
        response = github_api.<method>(...)

    with allure.step("Validate response"):
        assert_status_code(response.status_code, <expected>)
        ...
```

### Class-based (only when matching an existing file that uses it)

```python
@allure.epic("Repository API")
@allure.feature("<Feature Name>")
class Test<FeatureName>:

    @allure.title("<Test title from plan>")
    def test_<snake_case_title>(self, github_api, shared_repository):
        ...
```

Do not mix styles within the same file.

---

# Mapping Test Plan Fields to Code

* **Feature-level `Prepare`** → reuse an existing fixture (`github_api`, `created_repositories`, `shared_repository` in `tests/api_Tests/conftest.py`) if it already provides the needed setup. Only add a new fixture to `conftest.py` if none of the existing ones fit.
* **Feature-level `Clean`** → must be handled by fixture teardown (`yield` + cleanup code), not repeated per-test. Prefer `created_repositories` (auto-deletes tracked repos) when the test creates its own repository.
* **`Prepare test` / `Clean test`** (per-test) → implement inline within the test using `allure.step(...)` blocks, or a function-scoped fixture only if reused across multiple tests in the same file.
* **`Type`** (`positive|negative|boundary|validation|authorization|error`) → does not map to a pytest marker directly; it informs test design only. Optionally reflect it via `@allure.tag("<type>")`.
* **`Steps`** → translate each numbered step into request calls using the API client/wrapper (`github_api.<method>(...)` or a direct `ApiClient` call when testing something the wrapper doesn't support, e.g. invalid auth). Wrap each logical action in `allure.step(...)`.
* **`Expected`** → translate into assertions using `utils/assertions_api.py` helpers (`assert_status_code`, `assert_json_value`, `assert_json_key_exists`, `assert_header_exists`, `assert_response_time`) rather than raw `assert` statements. Attach the response body via `flows/api/api_flowes.py::attach_response(body)` (reuse this helper instead of duplicating `allure.attach(json.dumps(...))` inline).

---

# PLAN_TYPE / Type → Pytest Markers

Every implemented test must be marked `@pytest.mark.api` and `@pytest.mark.ai_test`.

The `ai_test` marker identifies tests generated by this skill, distinguishing them from manually authored tests. Apply it to every test this skill creates, with no exceptions.

Additionally, map the feature's `Plan type` to a marker:

* `SANITY` → `@pytest.mark.sanity`
* `SMOKE` → `@pytest.mark.smoke`
* `REGRESSION` → `@pytest.mark.regression`
* `MIXED` → do not apply a single blanket marker; instead, mark each individual test with whichever of `sanity`/`smoke`/`regression` best matches that specific test's role (e.g. a core happy-path test in a MIXED plan may be `smoke`, while an edge-case test may be `regression`).

If the `sanity` marker or the `ai_test` marker is not yet registered in `pytest.ini`, add it to the `markers` list before using it. Never use an unregistered marker.

---

# Framework Extension Rules

The test plan represents full QA requirements and may exceed current framework capability. When implementing:

* If an existing API client method (e.g. `GithubApi.update_repository`) does not support a field/parameter required by the test plan, extend that method to accept it (e.g. add `**kwargs` or explicit optional parameters merged into the request body) rather than working around it with raw `ApiClient` calls, unless the test itself is specifically about bypassing the wrapper (e.g. testing raw/invalid input).
* Keep extensions backward-compatible: existing callers of the method must continue to work unchanged.
* If a new fixture is required (e.g. a repository in a specific state, an organization-owned repository, a low-privilege token), add it to `tests/api_Tests/conftest.py`, following the existing fixture patterns (scope, cleanup via `yield`).
* If a new assertion helper is required, add it to `utils/assertions_api.py` following the existing function signature style (`assert_<thing>(actual, expected, ...) -> None`, raising a clear `AssertionError` message).
* Do not modify unrelated framework behavior while extending it.

---

# Handling Clarification-Flagged Tests

If a test's `Expected` section states that behavior is undocumented and "requires clarification":

* Do **not** implement that test.
* Do **not** guess at the expected behavior.
* Do **not** mark it `skip`/`xfail` in code.
* Track it and list it in your final summary to the user, including the test title and what clarification is needed.
* Ask the user how they want to proceed (e.g. investigate further, implement with an assumption, or leave unimplemented) before taking further action on those specific tests.

All other tests in the feature must still be implemented normally.

---

# Validation

After writing or modifying test file(s):

1. Run `pytest --collect-only <path to the affected test file(s)>` to confirm the tests collect without import or syntax errors.
2. If collection fails, fix the issue and re-validate before reporting completion.
3. Collection success is required, but running the tests live (which requires real GitHub API credentials and network access) is not required unless the user asks for it.

---

# Final Quality Check

Before reporting completion, verify:

* Every test in the feature's test list is implemented, except clarification-flagged tests.
* Test names match the test plan titles (translated to snake_case).
* Each test uses `allure.epic`, `allure.feature`, and a title (`allure.title` or `allure.dynamic.title`).
* Each test is marked `@pytest.mark.api`, `@pytest.mark.ai_test`, plus the correct plan-type marker.
* Assertions use `utils/assertions_api.py` helpers, not raw `assert`, where an existing helper covers the check.
* Response bodies are attached via `attach_response` (or `allure.attach` if no response body applies).
* Common preparation/cleanup uses fixtures; it is not duplicated inside every test.
* Test-specific preparation/cleanup is scoped to only the tests that need it.
* No existing tests were duplicated or broken.
* Any framework code extensions are backward-compatible.
* Any newly used pytest marker is registered in `pytest.ini`.
* `pytest --collect-only` succeeds for the new/modified file(s).
* Clarification-flagged tests are reported to the user, not implemented or invented.
