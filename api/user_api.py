from api import GitHubClient


class UserApi:
    def __init__(self, client):
        self.client = client

    def get_authenticated_user(self, endpoint):
        return self.client.get(endpoint)

    def update_user(self, endpoint, data):
        return self.client.patch(endpoint, data)
