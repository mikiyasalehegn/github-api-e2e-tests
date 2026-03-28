from api import GitHubClient


class UserApi:
    def __init__(self, client):
        self.client = client

    def get_authenticated_user(self):
        return self.client.get("/user")

    def update_user(self, data):
        return self.client.patch("/user", data)
