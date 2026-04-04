class RepoCollabApi:
    def __init__(self, client):
        self.client = client

    def get_repo_collaborator(self, owner, repo, username):
        return self.client.get(f"/repos/{owner}/{repo}/collaborators/{username}")

    def list_repo_collaborators(self, owner, repo):
        return self.client.get(f"/repos/{owner}/{repo}/collaborators")

    def check_repo_collaborator(self, owner, repo, username):
        return self.client.get(f"/repos/{owner}/{repo}/collaborators/{username}")

    def add_repo_collaborator(self, owner, repo, username, data=None):
        return self.client.put(f"/repos/{owner}/{repo}/collaborators/{username}", data)

    def remove_repo_collaborator(self, owner, repo, username):
        return self.client.delete(f"/repos/{owner}/{repo}/collaborators/{username}")

    def get_repo_permission_of_user(self, owner, repo, username):
        return self.client.get(f"/repos/{owner}/{repo}/collaborators/{username}/permission")
