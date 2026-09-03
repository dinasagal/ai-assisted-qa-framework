# FEATURE: Update Repository

**Description:** Verify that an authenticated user with sufficient permissions can update an existing GitHub repository's metadata and settings (such as name, description, homepage, and visibility) through the GitHub REST API `PATCH /repos/{owner}/{repo}` endpoint, and that invalid, unauthorized, or unsupported update attempts are rejected or handled as documented.

**Plan type:** REGRESSION

## Documentation

- [Update a repository](https://docs.github.com/en/rest/repos/repos#update-a-repository)
- [Get a repository](https://docs.github.com/en/rest/repos/repos#get-a-repository)
- [Create a repository for the authenticated user](https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user)
- [Delete a repository](https://docs.github.com/en/rest/repos/repos#delete-a-repository)
- [Get all repository topics](https://docs.github.com/en/rest/repos/repos#get-all-repository-topics)
- [Replace all repository topics](https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics)

## Test List

1. Update repository name with valid data
2. Update repository description with valid data
3. Update repository homepage with a valid URL
4. Update repository visibility from public to private
5. Update multiple repository settings in a single request
6. Archive a repository
7. Update repository with empty description
8. Update non-existing repository
9. Update repository with invalid owner
10. Update repository with invalid visibility value
11. Attempt to edit repository topics through the update repository endpoint
12. Update repository visibility as a non-owner when organization restricts visibility changes
13. Update repository without authentication
14. Update repository without sufficient permissions
15. Update `security_and_analysis` settings without required permission
16. Update a repository that has been renamed or moved

## Prepare

- Authenticate as a user holding a personal access token or fine-grained token with `repo` scope / `Administration` repository permissions (write) for the target repository.
- Create a repository with valid required data using `POST /user/repos` to serve as the target repository for update operations, unless a test specifies its own preparation.

## Tests

### Test 1 - Update repository name with valid data

**Type:** positive

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with an authenticated request (`Administration` write permission) and body `{"name": "<new-unique-name>"}`.

**Expected:**
Response status `200`. Response body `name` equals the new name and `full_name` reflects the new name. A subsequent `GET /repos/{owner}/{new-name}` returns `200` for the renamed repository.

---

### Test 2 - Update repository description with valid data

**Type:** positive

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"description": "<new description text>"}`.

**Expected:**
Response status `200`. Response body `description` equals the submitted value.

---

### Test 3 - Update repository homepage with a valid URL

**Type:** positive

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"homepage": "https://example.com"}`.

**Expected:**
Response status `200`. Response body `homepage` equals the submitted URL.

---

### Test 4 - Update repository visibility from public to private

**Type:** positive

**Prepare test:**
- Ensure the target repository's current visibility is public.

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"private": true}` (or equivalently `{"visibility": "private"}`).

**Expected:**
Response status `200`. Response body `private` is `true` and `visibility` is `private`. A subsequent `GET /repos/{owner}/{repo}` confirms the repository is private.

---

### Test 5 - Update multiple repository settings in a single request

**Type:** positive

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with a body containing multiple fields, e.g. `{"description": "<value>", "has_issues": false, "has_wiki": false}`.

**Expected:**
Response status `200`. Each field in the response body matches the submitted values.

---

### Test 6 - Archive a repository

**Type:** positive

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"archived": true}`.

**Expected:**
Response status `200`. Response body `archived` is `true`. A subsequent `GET /repos/{owner}/{repo}` confirms `archived` is `true`.

**Clean test:**
- Send `PATCH /repos/{owner}/{repo}` with body `{"archived": false}` to unarchive the repository before feature-level cleanup deletes it.

---

### Test 7 - Update repository with empty description

**Type:** boundary

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"description": ""}`.

**Expected:**
Response status `200`. Response body `description` is an empty string.

---

### Test 8 - Update non-existing repository

**Type:** negative

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` where `{repo}` is a repository name that does not exist under `{owner}`, using a valid request body.

**Expected:**
Response status `404`.

---

### Test 9 - Update repository with invalid owner

**Type:** negative

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` where `{owner}` does not correspond to any existing GitHub account, using a valid request body.

**Expected:**
Response status `404`.

---

### Test 10 - Update repository with invalid visibility value

**Type:** validation

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"visibility": "invalid-value"}`.

**Expected:**
Response status `200`. GitHub silently ignores unrecognized visibility values.visibility unchanged (`public` or `private`).

---

### Test 11 - Attempt to edit repository topics through the update repository endpoint

**Type:** validation

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"topics": ["example-topic"]}`.
2. Retrieve repository topics using `GET /repos/{owner}/{repo}/topics`.

**Expected:**
Per GitHub documentation, topics must be edited using the "Replace all repository topics" endpoint (`PUT /repos/{owner}/{repo}/topics`), not the update repository endpoint. The exact behavior of the update repository endpoint when a `topics` field is included in the request body (ignored vs. rejected) is not documented and requires clarification. Verify that repository topics remain unchanged by this request regardless of response status.

---

### Test 12 - Update repository visibility as a non-owner when organization restricts visibility changes

**Type:** authorization

**Prepare test:**
- Configure or use an organization-owned repository where the organization restricts changing repository visibility to organization owners.
- Authenticate as a member with `Administration` write permission on the repository but who is not an organization owner.

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"private": true}` (or an equivalent visibility change).

**Expected:**
Response status `422`, per documented behavior: a `422` error occurs if the organization restricts changing repository visibility to organization owners and a non-owner tries to change the value of `private`.

---

### Test 13 - Update repository without authentication

**Type:** authorization

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` without an `Authorization` header, using a valid request body.

**Expected:**
Response status `403`, per the documented status codes for this endpoint. The exact response body/message for a missing authentication credential is not detailed in the official documentation and requires clarification.

---

### Test 14 - Update repository without sufficient permissions

**Type:** authorization

**Prepare test:**
- Authenticate as a user or token that has read-only or no administrative access to the target repository (not `Administration` repository permissions write).

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with a valid request body.

**Expected:**
Response status `403`, consistent with the documented requirement that the "Update a repository" endpoint requires `Administration` repository permissions (write).

---

### Test 15 - Update `security_and_analysis` settings without required permission

**Type:** authorization

**Prepare test:**
- Authenticate as a user who has write access to the repository but is not an admin of the repository, nor an owner or security manager of the organization that owns it.

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` with body `{"security_and_analysis": {"advanced_security": {"status": "enabled"}}}`.

**Expected:**
Per GitHub documentation, using the `security_and_analysis` parameter requires admin permissions for the repository or being an owner/security manager of the organization that owns it. The precise error status/body when this permission is missing is not detailed in the official documentation and requires clarification. Verify that the `security_and_analysis` settings are not changed by an unauthorized request.

---

### Test 16 - Update a repository that has been renamed or moved

**Type:** error

**Prepare test:**
- Identify or create a scenario where the repository referenced by `{owner}/{repo}` has moved (e.g., the repository was previously renamed and the request uses the former owner/name), consistent with the documented `307` status.

**Steps:**
1. Send `PATCH /repos/{owner}/{repo}` using the repository's former owner/name.

**Expected:**
Response status `307`, redirecting the client to the repository's current location, consistent with the documented HTTP response status codes for this endpoint.

---

## Clean

- Delete any repositories created for these tests using `DELETE /repos/{owner}/{repo}`.
