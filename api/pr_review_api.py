class PullRequestReviewAPI:
    def __init__(self, client):
        self.client = client

    def get_pr_review_request(self, owner, repo, pr_number):
        return self.client.get(f"/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers")

    def request_pr_review(self, owner, repo, pr_number):
        return self.client.post(f"/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers")

    def remove_pr_review(self, owner, repo, pr_number):
        return self.client.delete(f"/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers")

