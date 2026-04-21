import pytest
from api import RepositoryApi
from base import BaseTest
from utils import USERNAME, COLLABORATOR_TOKEN
import logging

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
class TestCreateRepoWithInsufficientPermission(BaseTest):
    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.repo_api = RepositoryApi(self.client)

    def test_create_repo_with_insufficient_permission(self, create_temporary_repo):
        repo_name = create_temporary_repo

        # --------------------------- get repo ---------------------------
        repo_response = self.repo_api.get_repository(owner=USERNAME, repo=repo_name)
        logger.info(f"get repo response: {repo_response.json()}")
        assert repo_response.status_code == 200


        # ---------- delete repo with insufficient permission ------------
        no_permission_client = self.get_client(token=COLLABORATOR_TOKEN)
        no_permission_api = RepositoryApi(no_permission_client)

        delete_repo_response = self.repo_api.delete_repo(owner=USERNAME, repo_name=repo_name)
        # logger.info(f"delete repo response: {delete_repo_response.json()}")
        assert delete_repo_response.status_code == 403    # It seems a bug b/c this request deletes the with different token
