import time
import pytest
from api import RepositoryApi, GitHubClient
from test_data import UserTestData



@pytest.fixture(scope='class', autouse=True)
def create_temporary_repo(request):
    # Check for a custom marker on the class
    # Default: No README
    with_readme = False

    # Look for @pytest.mark.repo_config(with_readme=True)
    marker = request.node.get_closest_marker("repo_config")
    if marker:
        with_readme = marker.kwargs.get("with_readme", False)

    # Prepare the payload
    repository_name = f"tmp-repo-{int(time.time())}"
    payload = {
        "name": repository_name,
        "description": "Temp repo for E2E tests",
        "private": False,
        "auto_init": with_readme
    }

    # Create the repo
    client = GitHubClient(UserTestData.base_url, UserTestData.token)
    repo_api = RepositoryApi(client)
    repo_api.create_repo_for_authenticated_user(payload)

    # Provide data to the test class
    # We attach it to the class instance so tests can access self.repo_name
    if request.cls is not None:
        request.cls.repo_name = repository_name

    yield repository_name  # The tests run here

    # TEARDOWN: Delete the repo after the class finishes
    user_name = UserTestData.user_name
    repo_api.delete_repo(owner=user_name, repo_name=repository_name)
