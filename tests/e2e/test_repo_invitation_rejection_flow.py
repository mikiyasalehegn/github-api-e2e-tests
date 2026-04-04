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
        assert list_invitations_resp.json() == []

        check_user_invitation = self.invitation_api.get_user_invitations()
        assert check_user_invitation.status_code == 200

        return check_user_invitation.json() if is_invited else []


    def test_repo_invitation_rejection(self, create_temporary_repo):
        invitation_repo = create_temporary_repo

        # -------------------- Check invitation to the repo is empty --------------------
        invitee_client = self.get_client(token=COLLABORATOR_TOKEN)
        invitee_api = InvitationApi(invitee_client)
        invitations = self.check_repo_invitations(owner=USERNAME, repo=invitation_repo)
        assert invitations == []











