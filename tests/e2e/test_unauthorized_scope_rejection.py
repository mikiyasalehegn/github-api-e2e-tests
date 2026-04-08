from models import CreateRepoData
from test_data import RepoTestData
from utils import READ_ONLY_TOKEN
from api import RepositoryApi
from base import BaseTest
import logging


logger = logging.getLogger(__name__)



class TestUnauthorizedScopeRejection(BaseTest):
    def setup_method(self):
        super().setup_method()

        self.client = self.get_client(token=READ_ONLY_TOKEN)
        self.repo_api = RepositoryApi(self.client)

    def test_unauthorized_scope_rejection(self):

        # -------------- Create repository with unauthorized token --------------
        payload = CreateRepoData(repo_name=RepoTestData.repo_name, description=RepoTestData.description
                                 , path=RepoTestData.homepage, private=True)
        response = self.repo_api.create_repo_for_authenticated_user(data=payload.to_dict())

        # -------------- Verify that the user is unauthorized --------------
        logger.info(f"Create repo response data {response.text}")
        assert response.status_code == 403



