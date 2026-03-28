from api import UserApi, RepositoryApi
from base import BaseTest
from utils import assert_data_schema
from models import get_user_data_schema, UpdateUserDataModel, UpdateUserResponse, GetUserResponse, GetRepoResponse
from test_data import UserTestData


class TestUserInfoHappyFlow(BaseTest):
    def setup_method(self):
        # IMPORTANT: Call the parent setup first!
        super().setup_method()

        self.client = self.get_client()
        self.user_api = UserApi(self.client)
        self.repo_api = RepositoryApi(self.client)

    def test_get_authenticated_user(self):
        response = self.user_api.get_authenticated_user()
        user_res_data = GetUserResponse(response.json())

        assert response.status_code == 200
        assert_data_schema(response, get_user_data_schema)
        assert user_res_data.login == UserTestData.user_name
        assert user_res_data.type == UserTestData.user_type

    def test_update_authenticated_user(self):
        update_user_model = UpdateUserDataModel(twitter_username=UserTestData.twitter_username, bio=UserTestData.bio)
        response = self.user_api.update_user(update_user_model.to_dict())
        user_res_data = UpdateUserResponse(response.json())

        assert response.status_code == 200
        assert_data_schema(response, get_user_data_schema)
        assert user_res_data.twitter_username == UserTestData.twitter_username
        assert user_res_data.bio == UserTestData.bio

    def test_users_repository(self):
        response = self.repo_api.get_repo_for_authenticated_user()
        repo_res_data = GetRepoResponse(response.json()[0])
        assert response.status_code == 200
        assert repo_res_data.owner == UserTestData.user_name
        assert UserTestData.user_name in repo_res_data.full_name
