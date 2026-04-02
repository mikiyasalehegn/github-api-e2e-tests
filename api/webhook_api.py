class WebhookApi:
    def __init__(self, client):
        self.client = client

    def create_github_webhook(self, owner, repo, data):
        return self.client.post(f"/repos/{owner}/{repo}/hooks", data)

    def ping_webhook(self, owner, repo, hook_id):
        return self.client.post(f"/repos/{owner}/{repo}/hooks/{hook_id}/pings", payload={})

    def get_github_webhook(self, owner, repo, hook_id):
        return self.client.get(f"/repos/{owner}/{repo}/hooks/{hook_id}")

    def update_github_webhook(self, owner, repo, hook_id, data):
        return self.client.patch(f"/repos/{owner}/{repo}/hooks/{hook_id}", data)

    def delete_github_webhook(self, owner, repo, hook_id):
        return self.client.delete(f"/repos/{owner}/{repo}/hooks/{hook_id}")
