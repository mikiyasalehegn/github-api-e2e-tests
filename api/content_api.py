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

    def get_repository_content(self, owner, repo, path, ref=None):
        params = {"ref": ref} if ref else {}
        return self.client.get(f"/repos/{owner}/{repo}/contents/{path}", data=params)

    def update_file(self, owner, repo, path, data):
        return self.client.put(f"/repos/{owner}/{repo}/contents/{path}", payload=data)


    def update_repo_file(self, owner, repo, new_line_content, path, line_index=0, branch="main"):
        # 1. GET CURRENT CONTENT AND SHA
        resp = self.get_repository_content(owner, repo, path=path, ref=branch)
        resp.raise_for_status()
        file_data = resp.json()

        current_sha = file_data["sha"]
        # GitHub returns content as a Base64 string with newlines, we must clean it
        raw_content = base64.b64decode(file_data["content"]).decode("utf-8")

        # 2. MODIFY LINE ONE
        lines = raw_content.splitlines()
        if lines:
            lines[line_index] = new_line_content
        else:
            lines = [new_line_content]

        # Re-join with newlines
        updated_content_str = "\n".join(lines)
        updated_content_b64 = base64.b64encode(updated_content_str.encode("utf-8")).decode("utf-8")

        # 3. PUT THE UPDATE
        data = {
            "message": "Update first line of README",
            "content": updated_content_b64,
            "sha": current_sha,  # MANDATORY
            "branch": branch
        }

        update_resp = self.update_file(owner, repo, path=path, data=data)
        return update_resp