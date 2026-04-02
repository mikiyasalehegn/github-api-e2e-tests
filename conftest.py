import time
import pytest
from api import RepositoryApi, GitHubClient
from test_data import UserTestData



@pytest.fixture(scope='class', autouse=True)
def create_temporary_repo(request):
    # create repo using public api
    user_name = UserTestData.user_name
    repository_name = f"tmp-repo-{int(time.time())}"
    client = GitHubClient(UserTestData.base_url, UserTestData.token)
    repo_api = RepositoryApi(client)
    payload = {"name": repository_name, "description": "Temp repo for E2E tests", "private": False}
    repo_api.create_repo_for_authenticated_user(payload)

    # 4. Provide data to the test class
    # We attach it to the class instance so tests can access self.repo_name
    if request.cls is not None:
        request.cls.repo_name = repository_name

    yield repository_name  # The tests run here

    # TEARDOWN: Delete the repo after the class finishes
    repo_api.delete_repo(owner=user_name, repo_name=repository_name)
