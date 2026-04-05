import time
from utils import USERNAME, COLLABORATOR, COLLABORATOR_TOKEN
import pytest
import logging
from base import BaseTest
from api import RepoCollabApi, InvitationApi


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
class TestRepoInvitationRejectionFlow(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.invitation_api = InvitationApi(self.client)

    def check_repo_invitations(self, owner, repo, is_invited=False):
        list_invitations_resp = self.invitation_api.list_repo_invitations(owner=owner, repo=repo)
        assert list_invitations_resp.status_code == 200
        assert list_invitations_resp.json() == [] if is_invited == False else list_invitations_resp.json()

        check_user_invitation = self.invitation_api.get_user_invitations()
        logger.info(f"check_user_invitation: {check_user_invitation.text}")
        assert check_user_invitation.status_code == 200

        if is_invited:
            return check_user_invitation.json()
        else:
            return []


    def test_repo_invitation_rejection(self, create_temporary_repo):
        invitation_repo = create_temporary_repo

        # -------------------- Check invitation to the repo is empty --------------------
        invitations = self.check_repo_invitations(owner=USERNAME, repo=invitation_repo)
        assert invitations == []

        # -------------------- Test invite user to the repo --------------------
        add_collaborator_api = RepoCollabApi(self.client)
        invite_user_resp = add_collaborator_api.add_repo_collaborator(owner=USERNAME, repo=invitation_repo,
                                                                      username=COLLABORATOR)
        assert invite_user_resp.status_code == 201
        assert invite_user_resp.json()["invitee"]["login"] == COLLABORATOR
        invitation_id = invite_user_resp.json()["id"]
        time.sleep(2)

        # -------------------- Check user is invited --------------------
        invitee_client = self.get_client(token=COLLABORATOR_TOKEN)
        invitee_api = InvitationApi(invitee_client)
        invitations = invitee_api.get_user_invitations()
        assert invitations.status_code == 200
        logger.info(f"user invitations resp: {invitations.json()}")

        # -------------------- Decline invitation --------------------
        decline_invitation_resp = invitee_api.decline_invitation(invitation_id=invitations.json()[0]["id"])
        assert decline_invitation_resp.status_code == 204

        # -------------------- Delete invitation --------------------
        delete_invitation_resp = self.invitation_api.delete_invitation(owner=USERNAME, repo=invitation_repo,
                                                                       invitation_id=invitation_id)
        assert delete_invitation_resp.status_code == 204













