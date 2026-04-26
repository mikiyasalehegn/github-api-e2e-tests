class PrCommentApi:
    def __init__(self, client):
        self.client = client

    def create_pr_review_comment(self, owner, repo, pr_number, data):
        return self.client.post(f"/repos/{owner}/{repo}/pulls/{pr_number}/comments", payload=data)