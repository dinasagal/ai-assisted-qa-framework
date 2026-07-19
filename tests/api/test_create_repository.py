import uuid


def test_create_repository(github_api):

    repo_name = f"automation-{uuid.uuid4().hex[:8]}"

    response = github_api.create_repository(repo_name)

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == repo_name