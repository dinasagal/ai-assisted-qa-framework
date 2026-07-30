import json
import allure

from typing import Any

def attach_response(body: Any) -> None:
    allure.attach(
        json.dumps(body, indent=2),
        name="Response Body",
        attachment_type=allure.attachment_type.JSON,
    )