class PullRequestApi:
    def __init__(self, client):
        self.client = client

    def create_pull_request(self, owner, repo, data):
        return self.client.post(f"/repos/{owner}/{repo}/pulls", payload=data)

    def merge_pull_request(self, owner, repo, pr_number, commit_message="Merging via Automation"):
        payload = {"commit_message": commit_message, "commit_title": "merge"}
        return self.client.put(f"/repos/{owner}/{repo}/pulls/{pr_number}/merge", payload=payload)

    def get_merged_pull_request(self, owner, repo, pr_number):
        return self.client.get(f"/repos/{owner}/{repo}/pulls/{pr_number}/merge")

    def get_pull_request(self, owner, repo, pr_number):
        return self.client.get(f"/repos/{owner}/{repo}/pulls/{pr_number}")
