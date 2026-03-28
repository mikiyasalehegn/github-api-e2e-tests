from http.client import responses

from base import BaseTest
from api import RepositoryApi
from models import CreateRepoData, create_repo_schema, CreateRepoResponse, UpdateRepoData
from models.repo_data_schema.repo_testing_data import GetRepoResponse
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

    def test_get_a_repository(self):
        response = self.repo_api.delete_repo(owner=UserTestData.user_name, repo_name=RepoTestData.new_repo_name)
        get_repo_data = GetRepoResponse(response.json())
        get_repo_schema = create_repo_schema

        assert response.status_code == 200
        assert_data_schema(response, get_repo_schema)
        assert get_repo_data.name == RepoTestData.new_repo_name
        assert get_repo_data.owner == UserTestData.user_name

    def test_delete_repository(self):
        response = self.repo_api.delete_repo(owner=UserTestData.user_name, repo_name=RepoTestData.new_repo_name)
        assert response.status_code == 204

        # assert using get repo request
        resp = self.repo_api.delete_repo(owner=UserTestData.user_name, repo_name=RepoTestData.new_repo_name)
        assert response.status_code == 404


