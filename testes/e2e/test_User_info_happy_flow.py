import pytest
from api import UserApi
from base import BaseTest

class TestUserInfoHappyFlow(BaseTest):

    def test_get_authenticated_user(self):
        client = self.get_client()
        user_api = UserApi(client)
        response = user_api.get_authenticated_user(endpoint="/user")

        assert response.status_code == 200


