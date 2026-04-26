import requests


class GitHubClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, endpoint, data=None):
        return requests.get(self.base_url + endpoint, headers=self.headers, data=data)

    def post(self, endpoint, payload):
        return requests.post(self.base_url + endpoint, json=payload, headers=self.headers)

    def patch(self, endpoint, payload=None):
        return requests.patch(self.base_url + endpoint, json=payload, headers=self.headers)

    def put(self, endpoint, payload=None):
        return requests.put(self.base_url + endpoint, json=payload, headers=self.headers)

    def delete(self, endpoint, payload=None):
        return requests.delete(self.base_url + endpoint, headers=self.headers, json=payload)