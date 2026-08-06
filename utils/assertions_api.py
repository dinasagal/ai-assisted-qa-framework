from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def assert_status_code(actual_status: int, expected_status: int) -> None:
    """Assert that an HTTP status code matches the expected value."""

    assert (
        actual_status == expected_status
    ), f"Expected status code {expected_status}, but got {actual_status}."


def assert_response_time(actual_ms: float, max_ms: float) -> None:
    """Assert that response time is under or equal to a defined threshold in ms."""

    assert actual_ms <= max_ms, f"Expected response time <= {max_ms}ms, but got {actual_ms}ms."


def assert_header_exists(headers: Mapping[str, str], header_name: str) -> None:
    """Assert that a header exists in a response header map (case-insensitive)."""

    normalized_headers = {key.lower(): value for key, value in headers.items()}
    assert (
        header_name.lower() in normalized_headers
    ), f"Expected header '{header_name}' to exist, but it was not found."


def assert_json_key_exists(payload: Mapping[str, Any], key_path: str) -> None:
    """Assert that a dot-separated JSON key path exists in a payload."""

    _get_by_path(payload, key_path)


def assert_json_value(payload: Mapping[str, Any], key_path: str, expected_value: Any) -> None:
    """Assert that the value at a dot-separated JSON key path matches expected."""

    actual_value = _get_by_path(payload, key_path)
    assert (
        actual_value == expected_value
    ), f"Expected JSON value at '{key_path}' to be {expected_value!r}, but got {actual_value!r}."


def _get_by_path(payload: Mapping[str, Any], key_path: str) -> Any:
    current: Any = payload
    traversed: list[str] = []

    for part in key_path.split("."):
        traversed.append(part)
        if not isinstance(current, Mapping):
            joined_path = ".".join(traversed[:-1]) or "<root>"
            raise AssertionError(
                f"Expected '{joined_path}' to be a JSON object while resolving '{key_path}'."
            )

        if part not in current:
            raise AssertionError(f"Expected JSON key path '{key_path}' to exist, missing '{part}'.")

        current = current[part]

    return current