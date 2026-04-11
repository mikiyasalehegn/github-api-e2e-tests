import base64


class ContentApi:
    def __init__(self, client):
        self.client = client

    def create_file(self, owner, repo, path, message, content, branch):
        # GitHub requires the content to be base64 encoded strings
        base64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

        payload = {
            "message": message,
            "content": base64_content,
            "branch": branch
        }

        # Use your GitHubClient to send the PUT request
        return self.client.put(f"/repos/{owner}/{repo}/contents/{path}", payload=payload)