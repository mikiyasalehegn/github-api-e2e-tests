class RepositoryApi:
    def __init__(self, client):
        self.client = client

    def get_repository(self, owner, repo):
        return self.client.get(f"/repos/{owner}/{repo}")

    def create_repo_for_authenticated_user(self, data):
        return self.client.post("/user/repos", data)

    def get_repo_for_authenticated_user(self):
        return self.client.get("/user/repos")

    def update_repository(self, owner, repo, data):
        return self.client.patch(f"/{owner}/{repo}", data)

    def delete_repo(self, owner, repo_name):
        return self.client.delete(f"/repos/{owner}/{repo_name}")