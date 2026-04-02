class IssueApi:
    def __init__(self, client):
        self.client = client

    def get_issue(self, owner, repo, issue_number):
        return self.client.get(f"/repos/{owner}/{repo}/issues/{issue_number}")

    def create_issue(self, owner, repo, data):
        return self.client.post(f"/repos/{owner}/{repo}/issues", data)

    def update_issue(self, owner, repo, issue_number, data):
        return self.client.patch(f"/repos/{owner}/{repo}/issues/{issue_number}", data)

    def lock_issue(self, owner, repo, issue_number, data):
        return self.client.put(f"/repos/{owner}/{repo}/issues/{issue_number}/lock", data)

    def unlock_issue(self, owner, repo, issue_number):
        return self.client.delete(f"/repos/{owner}/{repo}/issues/{issue_number}/lock")
