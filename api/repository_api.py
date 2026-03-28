

class RepositoryApi:
    def __init__(self, client):
        self.client = client

    def get_repo_for_authenticated_user(self):
        return self.client.get("/user/repos")