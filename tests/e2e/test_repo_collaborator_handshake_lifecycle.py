import time
from utils import USERNAME
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
        self.invitation_api = InvitationApi(self.client)


    def test_repo_collaborator_handshake_flow(self, create_temporary_repo):

        time.sleep(1)
        # -------------------- Get repo collaborators --------------------
        collab_temp_repo = create_temporary_repo

        response = self.repo_collab_api.list_repo_collaborators(owner=USERNAME, repo=collab_temp_repo)
        logger.info(f"list_repo_collaborators response: {response.text}")
        assert response.status_code == 200
        assert len(response.json()) == 1


        # -------------------- Add repo collaborators --------------------
        # add_repo_collab_response = self.repo_collab_api.add_repo_collaborator(owner=USERNAME, repo=collab_temp_repo,
        #                                                                       username=USERNAME)




