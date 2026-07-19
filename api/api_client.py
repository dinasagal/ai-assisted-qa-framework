import requests


class ApiClient:

    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def get(self, endpoint):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
        )

    def post(self, endpoint, json):
        return requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=json,
        )

    def put(self, endpoint, json):
        return requests.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=json,
        )

    def delete(self, endpoint):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
        )