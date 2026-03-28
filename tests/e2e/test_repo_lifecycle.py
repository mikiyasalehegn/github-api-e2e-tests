from base import BaseTest
from api import RepositoryApi
from models import CreateRepoData, create_repo_schema, CreateRepoResponse, UpdateRepoData
from test_data import RepoTestData, UserTestData
from utils import assert_data_schema


class TestRepoLifecycle(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.repo_api = RepositoryApi(self.client)

    def test_create_repository(self):
        payload = CreateRepoData(repo_name=RepoTestData.repo_name, description=RepoTestData.description
                                 , path=RepoTestData.homepage)
        response = self.repo_api.create_repo_for_authenticated_user(payload.to_dict())
        create_repo_res = CreateRepoResponse(response.json())

        assert response.status_code == 201
        assert_data_schema(response, create_repo_schema)
        assert create_repo_res.name == RepoTestData.repo_name
        assert create_repo_res.description == RepoTestData.description
        assert create_repo_res.path == RepoTestData.homepage
        assert create_repo_res.private == False

    def test_update_repository(self):
        payload = UpdateRepoData(new_repo_name=RepoTestData.new_repo_name,
                                 new_description=RepoTestData.new_repo_description)
        response = self.repo_api.update_repository(owner=UserTestData.user_name, repo=RepoTestData.repo_name,
                                                   data=payload.to_dict())
        create_repo_res = CreateRepoResponse(response.json())

        assert response.status_code == 200
        assert_data_schema(response, create_repo_schema)
        assert create_repo_res.name == RepoTestData.new_repo_name
        assert create_repo_res.description == RepoTestData.new_repo_description

    # def test_delete_repository(self):


