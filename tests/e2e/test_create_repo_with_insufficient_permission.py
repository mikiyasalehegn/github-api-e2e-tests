import pytest
from api import RepositoryApi
from base import BaseTest
from utils import USERNAME
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








