import time
from utils import USERNAME, COLLABORATOR, COLLABORATOR_TOKEN
import pytest
import logging
from base import BaseTest
from api import RepoCollabApi, InvitationApi


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
class TestRepoCollaboratorHandshakeFlow(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.repo_collab_api = RepoCollabApi(self.client)

    def check_repo_collaborators(self, expected_collabs, repo_name, iscollabadded = False):
        # list repo collaborators
        response = self.repo_collab_api.list_repo_collaborators(owner=USERNAME, repo=repo_name)
        logger.info(f"list_repo_collaborators response: {response.text}")
        assert response.status_code == 200
        assert len(response.json()) == expected_collabs
        collabs = [x["login"] for x in response.json()]

        # check if the user is repo collaborator
        if iscollabadded:
            check_repo_collab_resp = self.repo_collab_api.check_repo_collaborator(owner=USERNAME, repo=repo_name,
                                                                                  username=COLLABORATOR)
            assert check_repo_collab_resp.status_code == 204

        return collabs


    def test_repo_collaborator_handshake_flow(self, create_temporary_repo):

        time.sleep(1)
        collab_temp_repo = create_temporary_repo

        # -------------------- Get repo collaborators --------------------
        self.check_repo_collaborators(expected_collabs=1, repo_name=collab_temp_repo)

        # -------------------- Add repo collaborators --------------------

        add_repo_collab_response = self.repo_collab_api.add_repo_collaborator(owner=USERNAME, repo=collab_temp_repo,
                                                                              username=COLLABORATOR)
        logger.info(f"add_repo_collaborator response: {add_repo_collab_response.text}")
        assert add_repo_collab_response.status_code == 201
        assert add_repo_collab_response.json()["invitee"]["login"] == COLLABORATOR
        invitation_id=add_repo_collab_response.json()["id"]

        # -------------------- Accept invitation --------------------

        invitation_client = self.get_client(token=COLLABORATOR_TOKEN)
        accept_invitation_api = InvitationApi(invitation_client)
        accept_invitation_response = accept_invitation_api.accept_invitation(invitation_id=invitation_id)
        logger.info(f"accept_invitation response: {accept_invitation_response.text}")

        assert accept_invitation_response.status_code == 204

        # -------------------- check if the collaborator is added --------------------
        collaborators = self.check_repo_collaborators(expected_collabs=2, repo_name=collab_temp_repo,
                                                      iscollabadded = True)
        assert USERNAME in collaborators
        assert COLLABORATOR in collaborators

        # -------------------- Remove repo collaborator --------------------

        remove_repo_collab_response = self.repo_collab_api.remove_repo_collaborator(owner=USERNAME, repo=collab_temp_repo,
                                                                                    username=COLLABORATOR)
        assert remove_repo_collab_response.status_code == 204

        # -------------------- check if the collaborator is removed --------------------
        collaborators = self.check_repo_collaborators(expected_collabs=1, repo_name=collab_temp_repo)
        assert USERNAME in collaborators
        assert COLLABORATOR not in collaborators

