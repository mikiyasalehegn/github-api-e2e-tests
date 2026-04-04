class InvitationApi:
    def __init__(self, client):
        self.client = client

    def get_user_invitations(self):
        return self.client.get(f"/user/repository_invitations")

    def list_repo_invitations(self, owner, repo):
        return self.client.get(f"/repos/{owner}/{repo}/invitations")

    def update_invitation(self, owner, repo, invitation_id, data):
        return self.client.patch(f"/repos/{owner}/{repo}/invitations/{invitation_id}", data)

    def accept_invitation(self, invitation_id):
        return self.client.patch(f"/user/repository_invitations/{invitation_id}")

    def decline_invitation(self, invitation_id):
        return self.client.delete(f"/user/repository_invitations/{invitation_id}")

    def delete_invitation(self, owner, repo, invitation_id):
        return self.client.delete(f"/repos/{owner}/{repo}/invitations/{invitation_id}")
