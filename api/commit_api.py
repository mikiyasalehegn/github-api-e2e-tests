class CommitApi:
    def __init__(self, client):
        self.client = client

    def get_commit(self, owner, repo, ref):
        return self.client.get(f"/repos/{owner}/{repo}/commits/{ref}")

    def list_commits(self, owner, repo):
        return self.client.get(f"/repos/{owner}/{repo}/commits")

    def get_commit_comment(self, owner, repo, comment_id):
        return self.client.get(f"/repos/{owner}/{repo}/comments/{comment_id}")

    def list_commit_comments(self, owner, repo, commit_sha):
        return self.client.get(f"/repos/{owner}/{repo}/commits/{commit_sha}/comments")

    def update_commit_comment(self, owner, repo, comment_id, content):
        return self.client.patch(f"/repos/{owner}/{repo}/comments/{comment_id}", data=content)

    def create_commit_comment(self, owner, repo, commit_sha, content):
        return self.client.post(f"/repos/{owner}/{repo}/commits/{commit_sha}/comments", payload=content)

    def delete_commit_comment(self, owner, repo, comment_id):
        return self.client.delete(f"/repos/{owner}/{repo}/comments/{comment_id}")
