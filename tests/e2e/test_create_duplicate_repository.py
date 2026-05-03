from api import RepositoryApi
from base import BaseTest
from models import CreateRepoData
from test_data import RepoTestData
import logging
from utils import USERNAME


logger = logging.getLogger(__name__)


class TestCreateDuplicateRepository(BaseTest):
    def setup_method(self):
        super().setup_method()
        client = self.get_client()
        self.repo_api = RepositoryApi(client)

    def test_duplicate_repository(self):
        # ----------------- create repository -----------------
        payload = CreateRepoData(repo_name=RepoTestData.repo_name, description=RepoTestData.description
                                 , path=RepoTestData.homepage)
        create_repo_resp = self.repo_api.create_repo_for_authenticated_user(payload.to_dict())
        logger.info(f"create_repo_resp: {create_repo_resp.text}")
        assert create_repo_resp.status_code == 201

        # ----------------- create repository with the same data -----------------
        duplicate_payload = CreateRepoData(repo_name=RepoTestData.repo_name, description=RepoTestData.description
                                 , path=RepoTestData.homepage)

        duplicate_repo_response = self.repo_api.create_repo_for_authenticated_user(duplicate_payload.to_dict())
        logger.info(f"duplicate_repo_resp: {duplicate_repo_response.text}")
        assert duplicate_repo_response.status_code == 422

        # ----------------- erase the existing repo -----------------
        delete_repo = self.repo_api.delete_repo(owner=USERNAME, repo_name=RepoTestData.repo_name)
        assert delete_repo.status_code == 204
