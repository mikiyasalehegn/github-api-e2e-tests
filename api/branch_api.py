class BranchApi:
    """Branch API class"""
    def __init__(self, client):
        self.client = client

    def get_branch_sha(self, owner, repo, branch='main'):
        return self.client.get(f"/repos/{owner}/{repo}/git/ref/heads/{branch}")

    def get_branch(self, owner, repo, branch='main'):
        return self.client.get(f"/repos/{owner}/{repo}/branches/{branch}")

    def create_branch(self, owner, repo, branch='main', data=None):
        return self.client.post(f"/repos/{owner}/{repo}/git/ref", data)

    def update_branch_protection(self, owner, repo, branch='main', data=None):
        return self.client.put(f"/repos/{owner}/{repo}/branches/{branch}/protection", data)

    def get_branch_protection(self, owner, repo, branch='main'):
        return self.client.get(f"/repos/{owner}/{repo}/branches/{branch}/protection")

    def delete_branch_protection(self, owner, repo, branch='main'):
        return self.client.delete(f"/repos/{owner}/{repo}/branches/{branch}/protection")
